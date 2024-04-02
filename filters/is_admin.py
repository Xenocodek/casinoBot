from database.db import DatabaseManager

from aiogram.filters import BaseFilter
from aiogram.types import Message

db = DatabaseManager()

class IsAdmin(BaseFilter):
    
    def __init__(self):
        pass

    async def __call__(self, message: Message) -> bool:
        """Asynchronously checks if the given message is sent by an admin.
        """

        # Get the user ID from the message
        self.user_id = message.from_user.id
        
        # Check if the admin ID exists and has only one value
        admin_id = await db.get_admins(self.user_id)

        if admin_id and len(admin_id) == 1:
            # Extract the admin ID
            extracted_admin_id = admin_id[0]

            # Check if the user ID matches the extracted admin ID
            return self.user_id == int(extracted_admin_id)
        
        # If the admin ID does not exist or has more than one value, return False
        return False