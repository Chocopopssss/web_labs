class UserRepository:
    def __init__(self):
        # Имитация базы данных в памяти
        self.users = {}
        self._id_counter = 1

    def get_all(self):
        return list(self.users.values())

    def get_by_id(self, user_id: int):
        return self.users.get(user_id)

    def get_by_email(self, email: str):
        for user in self.users.values():
            if user["email"] == email:
                return user
        return None

    def create(self, user_data: dict):
        user_id = self._id_counter
        self._id_counter += 1
        new_user = {"id": user_id, **user_data}
        self.users[user_id] = new_user
        return new_user

    def update(self, user_id: int, user_data: dict):
        user = self.users.get(user_id)
        if not user:
            return None
        # Обновляем только переданные поля
        for key, value in user_data.items():
            if value is not None:
                user[key] = value
        return user

    def delete(self, user_id: int):
        if user_id in self.users:
            return self.users.pop(user_id)
        return None
