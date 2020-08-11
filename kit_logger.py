from python import kt_helpers as kt
import time


class KitLogger:

    def __init__(self, user, member, group, email, password, state, zip_code, kit_count, local_zips):
        """Initializes all variables needed to execute this entire class"""
        super().__init__()
        self.user = user
        self.member = member
        self.group = group
        self.email = email
        self.password = password
        self.state = state
        self.zip_code = zip_code
        self.local_zips = local_zips
        self.iterations = int((kit_count / 10))
        self.used_location_ids = []
        self.location_data = []
        self.user_id = ''
        self.api_token = ''
        self.kits_logged = 0
        self.error = str('None')

    def activate(self):
        """Gets and sets user_id and api_token
           Chains each method
           :returns kits_logged, error
        """
        self.user_id, self.api_token = kt.get_authenticated(self)
        self.retrieve_locations()
        return self.kits_logged, self.error

    def retrieve_locations(self):
        """Gets location ids through api `POST` request
           Passes location_ids to send_drop_off method
        """
        location_ids = kt.retrieve_locations(self, self.user_id, self.api_token)
        self.send_drop_off(location_ids)

    def send_drop_off(self, location_ids):
        """Uses location_ids length to loop through user chose iterations
           Uses 10 member numbers per location
           Saves location_data to a txt file to send to the user in the telegram_bot.py file
           Catches exception if there are no location_ids
        """
        try:
            for location_id in location_ids:
                self.used_location_ids.append(location_id)
                self.location_data.append(f'.:Location: {location_id} :.')
                print(f':location>> id: {location_id} <<:')
                for _ in range(10):
                    if len(self.member) != 0:
                        result = kt.send_drop_off(
                            location_id,
                            self.member[0],
                            self.group,
                            self.user_id,
                            self.api_token
                        )
                        if result[0] is True:
                            del self.member[0]
                            self.kits_logged += 1
                            time.sleep(0.2)
                        else:
                            self.error = result[1]
                            self.location_data.append(
                                f'Error: Member number -> {self.member[0]} failed with error {self.error}')
                            del self.member[0]
                if self.error == 'None':
                    self.location_data.append('.:----Success----:.\n')
                self.location_data.append('-----------------------\n')
            logged_iterations = self.kits_logged / 10
            if logged_iterations != 0:
                if logged_iterations != self.iterations:
                    self.error = f'Only {str(logged_iterations)} unclaimed locations were here.'
            return self.update_user_files()
        except Exception as e:
            print(e)
            self.error = 'Location error: No unclaimed locations'
            return self.update_user_files()

    def update_user_files(self):
        """Writes location_data to file
           Writes used_location_ids to file
           Overwrites member_numbers.txt file with updated member list
        """
        with open('data/temp/location_data.txt', 'a') as file:
            file.write('\n'.join(self.location_data))
        with open('data/used/used_location_ids.txt', 'a') as file:
            for row in self.used_location_ids:
                file.write(f'{row}\n')
        with open(f'user_member_numbers/{self.user}/member_numbers.txt', 'w') as file:
            for row in self.member:
                file.write(f'{row}\n')
