from kubernetes import client, config 

class Matcher(object):

    def __init__(self, label_entry, svc_type=None):
        config.load_kube_config()
        self.v1 = client.CoreV1Api()
        self.v1beta1 = client.ExtensionsV1beta1Api()
        self.label = label_entry
        self.svc_type = svc_type

    def __match_deployments(self):
        matching = []
        for dep in self.v1beta1.list_deployment_for_all_namespaces().items:
            if self.label in dep.metadata.labels.items():
                matching.append(dep)
        return matching    

    def __match_pods(self):
        matching = []
        for pod in self.v1.list_pod_for_all_namespaces(watch=False).items:
            if self.label in pod.metadata.labels.items():
                matching.append(pod)
        return matching

    def __match_services(self):
        matching = []
        for svc in self.v1.list_service_for_all_namespaces(watch=False).items:
            if self.label in svc.metadata.labels.items() and (self._svc_type == None or self._svc_type == svc.spec.type):
                matching.append(svc)
        return matching

    def __set_label(self, label_entry):
        if type(label_entry) == dict:
            self._label = label_entry.items()[0]
        elif type(label_entry) == tuple:
            self._label = label_entry
        else:
            raise ValueError('Label must be a dictionary or key:value tuple')  

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, label_entry):
        self.__set_label(label_entry)

    @property
    def svc_type(self):
        return self._svc_type

    @label.setter
    def svc_type(self, svc_type):
        self._svc_type = svc_type

    @property
    def pods(self):
        return self.__match_pods()

    @property
    def services(self):
        return self.__match_services()

    @property
    def deployments(self):
        return self.__match_deployments()