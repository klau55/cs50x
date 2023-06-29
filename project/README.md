# Klau5's reservation tool
#### Video Demo:  https://youtu.be/LdZKtZKEkg0
#### Description:
I decided to make this project because i saw real life potential in it: In my building there actually is a common laundry room that one must reserve. The reservations there are made by actually coming to the laundry room, finding there a daily planner notebook and a pen. One must open the notebook, find the needed date and fill in their name on the time lines they want. In 2023 such approach feels miserable. That's why I decided to digitalize the process an solve an actual real life problem!


Klau5's reservation tool a web-page that building residents can use to reserve time for a laundry room. The project uses HTML, CSS, JS, Bootstrap, Python, Jinja, SQLite.
HTML pages are created via having one layout page and making other pages as layout page extensions. All HTML pages are in templates folder. Css and pictures are located in static folder. Everything else is free-flowing in parent folder
First web page (index.html) shows time availability via HTML date menu and time drop-down.
Second page(myreservations.html) allows user to see their own reservations and cancel any reservation time. Cancelling makes time instantly available for everyone again. This page automatically deletes reservation info for dates that have already passed.
When reserving or cancelling a time, a user gets an alert message stating if the action was successful.
Also web site has login, logout and register pages. They were taken from CS50 finance, later modernized and repurposed.
Additionally, there is an apology html that is used to describe a problem if an issue happened(like already existing username). This apology html doesn't have a meme picture, just CSS wrapped div text.
SQLite database includes users table with fields username and password. Passwords are hashed with werkzeug extension, just as with CS50 Finance.
Another SQL database is reservations. It has fields users, date and the reserved time. Time is stored in 0 to 5 value, where 10:00 to 12:00 time is eqvivalent to 0, 12:00 to 14:00 correlates with 1 etc.
Each user sees only their own reservations and can cancel only their reservations. But all users will see the same poll of available times.
The design is pretty basic and intuitive, as I have focused mostly on getting the backend to work flawlessly while interconnecting python with jinja and js. The design includes a bootstrap navigation bar. Most of the background design is done with static pictures.
