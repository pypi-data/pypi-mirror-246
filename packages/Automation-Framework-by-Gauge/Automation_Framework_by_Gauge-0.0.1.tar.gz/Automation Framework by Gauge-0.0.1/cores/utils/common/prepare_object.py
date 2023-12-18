from cores.model import RequestObj


class PrepareObj:

    @staticmethod
    def preparation(Model) -> RequestObj:
        return RequestObj(**Model)
