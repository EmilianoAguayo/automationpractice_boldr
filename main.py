from bot import ValidateWebPage
from models import UserProfile

url = "http://automationpractice.com/index.php"
gender = "mr"
first_name = "Francisco"
last_name = "Aguayo"
email = "microstudio.test02@gmail.com"
password = "password"
birthday = "1993/September/2"
sing_up = True
receive_info = True
company = "Company Name"
address_one = "First Address"
address_two = "Second Address"
city = "My City"
state = "Alaska"
post_code = "76110"
country = "United States"
additional_info = "Additional Information"
phone = "4422182340"
phone_mobile = "4426043076"
alias = "Emiliano"

user_profile = UserProfile(gender, first_name, last_name, email, password, birthday, sing_up,
                           receive_info, company, address_one, address_two, city, state, post_code,
                           country, additional_info, phone, phone_mobile, alias
                           )

bot_dev = ValidateWebPage(url, user_profile)
# bot_dev.create_account()
bot_dev.sign_in()
bot_dev.add_item_to_cart()
bot_dev.check_out()
bot_dev.sign_out()
