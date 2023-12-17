from redis.cluster import RedisCluster, ClusterNode
from redis import Redis
from typing import List, Tuple, Union

from redis.cluster import RedisCluster
from server_utils.redis.keys import TaskStatus

class RedisUtil:
    """The RedisUtil class is used to initialize a redis connection and operate on the redis server.
    """
    def __init__(self, cluster_mode: bool = False, redis_url: str = "localhost:6379", redis_cluster_nodes: List[str] = "", ttl: int = 7 * 24 * 60 * 60):
        """Init redis connection and set ttl

        Args:
            cluster_mode (bool, optional): true if the server uses Redis Cluster. Defaults to False.
            redis_url (_type_, optional): Defaults to "localhost:6379".
            redis_cluster_nodes (List[str], optional): Defaults to "".
            ttl (int, optional): Time To Live. Defaults to 7*24*60*60.
        """
        self.ttl = ttl  # Default ttl 7 days
        self._cluster_mode = cluster_mode
        self._redis_url = redis_url
        self._redis_cluster_nodes = redis_cluster_nodes
        
        self.conn = self.__connect__()
        print(f"Redis connection {self.conn}")
        if self.conn is None:
            print("Redis connection failure. cannot cache result result")

    def get_redis_data(self, key: str) -> dict:
        """_summary_

        Args:
            key (str): _description_

        Returns:
            dict: _description_
        """
        data = self.hgetall(key)
        if data:
            data = {key.decode("utf-8"): value for key, value in data.items()}
            try:
                return data
            except:
                return {}
        return {}

    def set_result(
            self, key: str, 
            status: int, 
            device_tokens: List[str], 
            gif_url: str = "",
            video_url: str = "",
            expiry = None,):
        """_summary_

        Args:
            key (str): _description_
            status (int): _description_
            device_tokens (List[str]): _description_
            gif_url (str, optional): _description_. Defaults to "".
            video_url (str, optional): _description_. Defaults to "".
            expiry (_type_, optional): _description_. Defaults to None.

        Raises:
            RedisException: _description_
        """
        if gif_url and video_url:
            value = {
                "status": status,
                "device_tokens": " ".join(device_tokens),
                "gif_url": gif_url,
                "video_url": video_url,
            }
        else:
            value = {
                "status": status,
                "device_tokens": " ".join(device_tokens),
            }
        self.hmset(key, value, expiry)

    def get_result(self, key: str) -> dict:
        """_summary_

        Args:
            key (str): _description_

        Returns:
            dict: _description_
        """
        data = self.hgetall(key)
        if data:
            data = {key.decode("utf-8"): value for key, value in data.items()}
            try:
                task_status = int(data["status"].decode("utf-8"))
                return dict(status=TaskStatus(task_status), result=data["result"])
            except:
                return {}
        return {}

    def hmset(self, key: str, value, expiry = None):
        """_summary_

        Args:
            key (str): _description_
            value (_type_): _description_
            expiry (_type_, optional): _description_. Defaults to None.
        """
        if expiry is None:
            expiry = self.ttl
        if self.conn:
            self.conn.hmset(self.__result_id__(key), value)
            self.conn.expire(self.__result_id__(key), expiry)

    def hgetall(self, key) -> dict:
        """_summary_

        Args:
            key (_type_): _description_

        Returns:
            dict: _description_
        """
        if self.conn:
            return self.conn.hgetall(self.__result_id__(key))
        return {}

    def start_process_task(
        self, task_id: str, device_tokens: str
    ):
        self.set_result(task_id, TaskStatus.in_process.value, device_tokens, 600) # 100 mins

    def cancel_process_task(
        self, task_id: str, device_tokens: str
    ):
        self.set_result(task_id, TaskStatus.cancelled.value, device_tokens)

    def done_task(
            self, 
            task_id: str, 
            device_tokens: List[str], 
            video_url: str = "", 
            gif_url: str = "",
    ):
        """_summary_

        Args:
            task_id (str): _description_
            device_tokens (List[str]): _description_
            video_url (str, optional): _description_. Defaults to "".
            gif_url (str, optional): _description_. Defaults to "".
        """
        print(f"Redis finished task {task_id} {TaskStatus.done.value}")
        self.set_result(task_id, 
                        TaskStatus.done.value, 
                        device_tokens,
                        video_url=video_url,
                        gif_url=gif_url,)

    def is_cancelled_task(self, task_id: str) -> bool:
        """_summary_

        Args:
            task_id (str): _description_

        Returns:
            bool: _description_
        """
        task_data = self.get_result(task_id)
        if hasattr(task_data, "status"):
            return task_data["status"].value == TaskStatus.cancelled.value
        return False

    def is_done_task(self, task_id: str) -> bool:
        """_summary_

        Args:
            task_id (str): _description_

        Returns:
            bool: _description_
        """
        task_data = self.get_result(task_id)
        if hasattr(task_data, "status"):
            return task_data["status"].value == TaskStatus.done.value
        return False

    def failed_task(self, task_id: str, device_tokens: List[str]):
        """_summary_

        Args:
            task_id (str): _description_
            device_tokens (List[str]): _description_
        """
        self.set_result(task_id, TaskStatus.failed.value, device_tokens)
    
    def __connect__(self) -> Union[Redis, RedisCluster]:
        """Connect to redis server based on cluster mode

        Returns:
            RedisCluster: _description_
        """
        if self._cluster_mode == True:
            nodes = []
            for url in self._redis_cluster_nodes:
                host, port = self.__parse_location(url)
                nodes.append(ClusterNode(host=host, port=port))
            return RedisCluster(startup_nodes=nodes, decode_responses=True)
        return Redis.from_url(self._redis_url)
    
    @staticmethod
    def __parse_location(path: str) -> Tuple[str, str]:
        """_summary_

        Args:
            path (str): _description_

        Raises:
            Exception: _description_

        Returns:
            Tuple[str, str]: _description_
        """
        parts = path.split(":")
        if len(parts) < 2:
            raise Exception("Invalid redis path")
        return parts[0], parts[1]