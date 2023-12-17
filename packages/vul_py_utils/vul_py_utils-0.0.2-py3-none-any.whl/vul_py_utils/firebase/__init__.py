"""
    This module contains Firebase Class to interact with Firebase.
"""

from datetime import datetime, timezone
from enum import Enum

from typing import Annotated, List
from firebase_admin import credentials, messaging, storage, firestore, initialize_app

from server_utils.redis.keys import TaskStatus

class Reaction(Enum):
    """ ArtWork Reaction """
    Neutral = 0
    Like = 1
    Dislike = 2


class Firebase:
    """ This class is used to interact with Firebase """
    def __init__(self, key_path: str, storage_bucket: str, app_name: str):
        firebase_cred = credentials.Certificate(key_path)
        firebase_app = initialize_app(firebase_cred, {"storageBucket": storage_bucket}, app_name)
        self.app = firebase_app
        self.db = firestore.client(app=firebase_app) # type: firestore.Firestore
        self.bucket = storage.bucket(app=firebase_app)

    def send_fcm_notification(self, task_id: str, 
                              video_result_url: str, gif_result_url: str, 
                              device_tokens: List[str])->None:
        """ Send FCM Notification to device_tokens """
        title = "Animation"
        body = "Your Animation is ready!"
        data = {
            "task_id": task_id,
            "video_result_url": video_result_url,
            "gif_result_url": gif_result_url,
        }
        self._push_fcm_notification(title, body, data, device_tokens)

    def pend_task(self, task_id: str, user_id: str, animation_dict: dict)->None:
        self.__init_art_work_to_firestore(task_id, TaskStatus.pending.value, user_id, animation_dict)

    def start_process_task(self, task_id: str, user_id: str)->None:
        self.__update_art_work_to_firestore(task_id, TaskStatus.in_process.value, user_id)

    def failed_task(self, task_id: str, user_id: str)->None:
        self.__update_art_work_to_firestore(task_id, TaskStatus.failed.value, user_id)

    def cancel_process_task(self, task_id: str, user_id: str)->None:
        self.__update_art_work_to_firestore(task_id, TaskStatus.cancelled.value, user_id)

    def done_task(self,
                  device_tokens: List[str], user_id: str, task_id: str,
                  mp4_video_result: bytes = b'', gif_result: bytes = b'')->tuple[str, str]:
        """ Update ArtWork to Firestore and Push Result to Google Cloud. """
        video_result_url, gif_result_url = self.__push_result_to_google_cloud(task_id, user_id, mp4_video_result, gif_result)
        self.__update_art_work_to_firestore(task_id, TaskStatus.done.value, user_id, video_result_url, gif_result_url)
        print(f"Firebase finished task {task_id} {TaskStatus.done.value}")
        self.send_fcm_notification(task_id, video_result_url, gif_result_url, device_tokens)
        return video_result_url, gif_result_url

    def get_art_work(self, user_id: str, task_id: str)->Annotated[dict, None]:
        """ Get ArtWork Information """
        doc_ref = self.db.collection("Processes").document(
            user_id).collection("ArtWork").document(task_id)
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()
        else:
            return None

    def get_all_art_work(self, user_id: str) -> List[dict]:
        """ Get All ArtWork Information """
        docs = self.db.collection("Processes").document(user_id).collection("ArtWork").stream()
        all_art_work = []
        for doc in docs:
            doc.to_dict()
            if doc.to_dict()["status"] in [TaskStatus.done.value, TaskStatus.pending.value, TaskStatus.in_process.value]:
                doc_dict = doc.to_dict()
                doc_dict["id"] = doc.id
                all_art_work.append(doc_dict)
        return all_art_work

    def edit_art_work_reaction(self, user_id: str, task_id: str, reaction: str)->dict:
        """ Edit ArtWork Reaction """
        doc_ref = self.db.collection("Processes").document(user_id).collection("ArtWork").document(task_id)
        doc = doc_ref.get()
        if doc.exists:
            doc_ref.set({"reaction": reaction}, merge=True)
            return doc_ref.get().to_dict()
            
    def _push_fcm_notification(self, title: str, body: str, data: dict[str:str], tokens: List[str])->None:
        """ Push FCM Notification to device_tokens """
        message = messaging.MulticastMessage(
            data=data,
            notification=messaging.Notification(title=title, body=body),
            tokens=tokens,
            android=messaging.AndroidConfig(notification=messaging.AndroidNotification(
                click_action="NAVIGATE_TO_ANIM_PREVIEW")))
        response = messaging.send_multicast(app=self.app, multicast_message=message) # type: messaging.BatchResponse
        if response.failure_count > 0:
            self.__log_fcm_error(tokens, response)
        
    def __log_fcm_error(self, tokens: List[str], response: messaging.BatchResponse)->None:
        """ Log FCM Error """
        if response.failure_count > 0:
            failed_tokens = []
            for idx, resp in enumerate(response.responses):
                if not resp.success:
                    print("[FCM Token] Error is", resp.exception)
                    # The order of responses corresponds to the order of the registration tokens
                    failed_tokens.append(tokens[idx])
            print(f"List of tokens that caused failures: {failed_tokens}")

    def __init_art_work_to_firestore(self,
                                     task_id: str,
                                     status: int,
                                     user_id: str,
                                     animation_dict: dict)->None:
        """ Init ArtWork Information to Firestore"""
        art_work_data = {
            **animation_dict,
            "status": status,
        }
        user_doc_ref = self.db.collection("Processes").document(user_id)
        doc_ref = user_doc_ref.collection("ArtWork").document(task_id)
        doc_ref.set(art_work_data, merge=True)

    def __update_art_work_to_firestore(self, task_id: str, status: int, user_id: str, video_result_url: str = "", gif_result_url: str = "")->None:
        """ Update Firebase """
        data = {
            "status": status,
            "video_url": video_result_url,
            "gif_url": gif_result_url,
            "updated_at": datetime.now(timezone.utc).strftime("%Y-%m-%d%H:%M:%S")
        }
        user_doc_ref = self.db.collection("Processes").document(user_id)
        doc_ref = user_doc_ref.collection("ArtWork").document(task_id)
        doc_ref.set(data, merge=True)

    def __push_result_to_google_cloud(self,
                                      task_id: str, user_id: str,
                                      video_result: bytes, gif_result: bytes, 
                                      video_extension: str = "mp4", gif_extension:str = "gif") -> tuple[str, str]:
        """ Push video_result and gif_result to Google Cloud Storage 
        Returns: (video_result_url, gif_result_url)
        """
        # Path to store on Cloud Storage
        # Upload video
        mp4_blob = self.bucket.blob(f"{user_id}/{task_id}/{task_id}.{video_extension}") 
        mp4_blob.upload_from_string(video_result)
        mp4_blob.make_public()
        # Upload gif
        gif_blob = self.bucket.blob(f"{user_id}/{task_id}/{task_id}.{gif_extension}")
        gif_blob.upload_from_string(gif_result)
        gif_blob.make_public()
        return mp4_blob.public_url, gif_blob.public_url