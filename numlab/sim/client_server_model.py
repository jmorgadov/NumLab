from queue import PriorityQueue
from typing import Callable, List


class Server:
    def __init__(self, func: Callable, cost: float = 1.0):
        self.func = func
        self.cost = cost


class ClientServerModel:
    def __init__(
        self,
        arrival_func: Callable,
        servers: List[Server],
        config: List[int],
        client_limit: int = None,
        time_limit: float = None,
    ):
        self.arrival_func = arrival_func
        if len(config) != len(servers):
            raise ValueError("config and servers must have same length")
        for conf in config:
            if conf <= 0:
                raise ValueError("config values must be positive")
        self.servers = servers
        self.config = config
        self.events = PriorityQueue()
        self.servers_queue = [0] * len(servers)
        self.servers_in_use = [0] * len(servers)
        self.time = 0.0
        self.clients = 0
        if client_limit is None and time_limit is None:
            raise ValueError("Either client_limit or time_limit must be specified")
        self.client_limit = client_limit
        self.time_limit = time_limit

    def run(self):
        self.time = 0
        self.clients = 0
        self.servers_queue = [0] * len(self.servers)
        self.servers_in_use = [0] * len(self.servers)
        while True:
            if self.events.empty():
                self.events.put((self.time + self.arrival_func(), 0))
            time, server = self.events.get()
            if self.time_limit is not None and time > self.time_limit:
                break
            self.time = time
            if server > 0:
                if self.servers_queue[server - 1]:
                    self.servers_queue[server - 1] -= 1
                    self.events.put(
                        (self.time + self.servers[server - 1].func(), server)
                    )
                else:
                    self.servers_in_use[server - 1] -= 1
            if server == len(self.servers):
                self.clients += 1
                if self.client_limit is not None and self.clients > self.client_limit:
                    break
                continue
            if server == 0:
                self.events.put((self.time + self.arrival_func(), 0))

            if self.servers_in_use[server] >= self.config[server]:
                self.servers_queue[server] += 1
            else:
                self.servers_in_use[server] += 1
                self.events.put((self.time + self.servers[server].func(), server + 1))
