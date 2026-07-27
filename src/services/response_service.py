class ResponseService:

    @staticmethod
    def success(data):

        return {

            "success": True,

            "data": data

        }

    @staticmethod
    def failure(message):

        return {

            "success": False,

            "message": message

        }