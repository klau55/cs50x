-- Keep a log of any SQL queries you execute as you solve the mystery.
interviews
| Ruth    | Sometime within ten minutes of the theft, I saw the thief get into a car in the bakery parking lot and drive away. If you have security footage from the bakery parking lot, you might want to look for cars that left the parking lot in that time frame.                                                          |
| Eugene  | I don't know the thief's name, but it was someone I recognized. Earlier this morning, before I arrived at Emma's bakery, I was walking by the ATM on Leggett Street and saw the thief there withdrawing some money.                                                                                                 |
| Raymond | As the thief was leaving the bakery, they called someone who talked to them for less than a minute. In the call, I heard the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow. The thief then asked the person on the other end of the phone to purchase the flight ticket. |

bakery licence plate logs
SELECT DISTINCT * FROM people JOIN bakery_security_logs ON bakery_security_logs.license_plate = people.license_plate WHERE people.license_plate IN(SELECT license_plate FROM bakery_security_logs WHERE month = '7' AND day = '28' AND hour = '10');

221103 | Vanessa | (725) 555-4692 | 2963008352      | 5P2BI95       | 260 | 2021 | 7     | 28  | 10   | 16     | exit     | 5P2BI95
243696 | Barry   | (301) 555-4174 | 7526138472      | 6P58WS2       | 262 | 2021 | 7     | 28  | 10   | 18     | exit     | 6P58WS2
396669 | Iman    | (829) 555-5269 | 7049073643      | L93JTIZ       | 265 | 2021 | 7     | 28  | 10   | 21     | exit     | L93JTIZ +
398010 | Sofia   | (130) 555-0289 | 1695452385      | G412CB7       | 264 | 2021 | 7     | 28  | 10   | 20     | exit     | G412CB7
449774 | Taylor  | (286) 555-6063 | 1988161715      | 1106N58       | 268 | 2021 | 7     | 28  | 10   | 35     | exit     | 1106N58 -
467400 | Luca    | (389) 555-5198 | 8496433585      | 4328GD8       | 263 | 2021 | 7     | 28  | 10   | 19     | exit     | 4328GD8 +
514354 | Diana   | (770) 555-1861 | 3592750733      | 322W7JE       | 266 | 2021 | 7     | 28  | 10   | 23     | exit     | 322W7JE +
560886 | Kelsey  | (499) 555-9472 | 8294398571      | 0NTHK55       | 267 | 2021 | 7     | 28  | 10   | 23     | exit     | 0NTHK55
686048 | Bruce   | (367) 555-5533 | 5773159633      | 94KL13X       | 261 | 2021 | 7     | 28  | 10   | 18     | exit     | 94KL13X +

withdrawals leggett street 28 7 2021
SELECT * from atm_transactions JOIN bank_accounts ON atm_transactions.account_number = bank_accounts.account_number JOIN people ON bank_accounts.person_id = people.id WHERE year = '2021' AND day = '28' AND month = '7' AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw';
| 267 | 49610011       | 2021 | 7     | 28  | Leggett Street | withdraw         | 50     | 49610011       | 686048    | 2010          | 686048 | Bruce   | (367) 555-5533 | 5773159633      | 94KL13X       |
| 336 | 26013199       | 2021 | 7     | 28  | Leggett Street | withdraw         | 35     | 26013199       | 514354    | 2012          | 514354 | Diana   | (770) 555-1861 | 3592750733      | 322W7JE       |
| 269 | 16153065       | 2021 | 7     | 28  | Leggett Street | withdraw         | 80     | 16153065       | 458378    | 2012          | 458378 | Brooke  | (122) 555-4581 | 4408372428      | QX4YZN3       |
| 264 | 28296815       | 2021 | 7     | 28  | Leggett Street | withdraw         | 20     | 28296815       | 395717    | 2014          | 395717 | Kenny   | (826) 555-1652 | 9878712108      | 30G67EN       |
| 288 | 25506511       | 2021 | 7     | 28  | Leggett Street | withdraw         | 20     | 25506511       | 396669    | 2014          | 396669 | Iman    | (829) 555-5269 | 7049073643      | L93JTIZ       |
| 246 | 28500762       | 2021 | 7     | 28  | Leggett Street | withdraw         | 48     | 28500762       | 467400    | 2014          | 467400 | Luca    | (389) 555-5198 | 8496433585      | 4328GD8       |
| 266 | 76054385       | 2021 | 7     | 28  | Leggett Street | withdraw         | 60     | 76054385       | 449774    | 2015          | 449774 | Taylor  | (286) 555-6063 | 1988161715      | 1106N58       |
| 313 | 81061156       | 2021 | 7     | 28  | Leggett Street | withdraw         | 30     | 81061156       | 438727    | 2018          | 438727 | Benista | (338) 555-6650 | 9586786673      | 8X428L0       |


who was leaving bakery at 10 + withdrew money on leggett
SELECT DISTINCT(name) FROM people JOIN bakery_security_logs ON bakery_security_logs.license_plate = people.license_plate WHERE people.license_plate IN(SELECT license_plate FROM bakery_security_logs WHERE month = '7' AND day = '28' AND hour = '10') AND name IN (SELECT name from people JOIN bank_accounts ON atm_transactions.account_number = bank_accounts.account_number JOIN atm_transactions ON bank_accounts.person_id = people.id WHERE year = '2021' AND day = '28' AND month = '7' AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw');
+--------+
|  name  |
+--------+
| Iman   |
| Taylor |
| Luca   |
| Diana  |
| Bruce  |
+--------+


Who called for less than 60 sec on that day
SELECT * FROM phone_calls JOIN people ON people.phone_number = phone_calls.caller WHERE name = 'Iman' OR name = 'Taylor' OR name = 'Luca' OR name = 'Diana' Or name = 'Bruce' AND day = '28' AND duration < 60;
| id  |     caller     |    receiver    | year | month | day | duration |   id   |  name  |  phone_number  | passport_number | license_plate |
| 233 | (367) 555-5533 | (375) 555-8161 | 2021 | 7     | 28  | 45       | 686048 | Bruce  | (367) 555-5533 | 5773159633      | 94KL13X       |
| 254 | (286) 555-6063 | (676) 555-6554 | 2021 | 7     | 28  | 43       | 449774 | Taylor | (286) 555-6063 | 1988161715      | 1106N58       | -
| 255 | (770) 555-1861 | (725) 555-3243 | 2021 | 7     | 28  | 49       | 514354 | Diana  | (770) 555-1861 | 3592750733      | 322W7JE       | -


SELECT * FROM flights JOIN airports ON flights.origin_airport_id = airports.id JOIN passengers ON passengers.flight_id = flights.id JOIN people ON people.passport_number = passengers.passport_number WHERE flights.year = '2021' AND flights. month = '7' AND flights. day = '29' AND passengers.passport_number = '5773159633';

+----+-------------------+------------------------+------+-------+-----+------+--------+----+--------------+-----------------------------+------------+-----------+-----------------+------+--------+-------+----------------+-----------------+---------------+
| id | origin_airport_id | destination_airport_id | year | month | day | hour | minute | id | abbreviation |          full_name          |    city    | flight_id | passport_number | seat |   id   | name  |  phone_number  | passport_number | license_plate |
+----+-------------------+------------------------+------+-------+-----+------+--------+----+--------------+-----------------------------+------------+-----------+-----------------+------+--------+-------+----------------+-----------------+---------------+
| 36 | 8                 | 4                      | 2021 | 7     | 29  | 8    | 20     | 8  | CSF          | Fiftyville Regional Airport | Fiftyville | 36        | 5773159633      | 4A   | 686048 | Bruce | (367) 555-5533 | 5773159633      | 94KL13X       |
+----+-------------------+------------------------+------+-------+-----+------+--------+----+--------------+-----------------------------+------------+-----------+-----------------+------+--------+-------+----------------+-----------------+---------------+

| id | origin_airport_id | destination_airport_id | year | month | day | hour | minute | id | abbreviation |          full_name          |    city    | flight_id | passport_number | seat |   id   |  name  |  phone_number  | passport_number | license_plate |
+----+-------------------+------------------------+------+-------+-----+------+--------+----+--------------+-----------------------------+------------+-----------+-----------------+------+--------+--------+----------------+-----------------+---------------+
| 36 | 8                 | 4                      | 2021 | 7     | 29  | 8    | 20     | 8  | CSF          | Fiftyville Regional Airport | Fiftyville | 36        | 1988161715      | 6D   | 449774 | Taylor | (286) 555-6063 | 1988161715      | 1106N58       |
+----+-------------------+------------------------+------+-------+-----+------+--------+----+--------------+-----------------------------+------------+-----------+-----------------+------+--------+--------+----------------+-----------------+---------------+

+----+-------------------+------------------------+------+-------+-----+------+--------+----+--------------+-----------------------------+------------+-----------+-----------------+------+--------+-------+----------------+-----------------+---------------+
| id | origin_airport_id | destination_airport_id | year | month | day | hour | minute | id | abbreviation |          full_name          |    city    | flight_id | passport_number | seat |   id   | name  |  phone_number  | passport_number | license_plate |
+----+-------------------+------------------------+------+-------+-----+------+--------+----+--------------+-----------------------------+------------+-----------+-----------------+------+--------+-------+----------------+-----------------+---------------+
| 18 | 8                 | 6                      | 2021 | 7     | 29  | 16   | 0      | 8  | CSF          | Fiftyville Regional Airport | Fiftyville | 18        | 3592750733      | 4C   | 514354 | Diana | (770) 555-1861 | 3592750733      | 322W7JE       |
+----+-------------------+------------------------+------+-------+-----+------+--------+----+--------------+-----------------------------+------------+-----------+-----------------+------+--------+-------+----------------+-----------------+---------------+

BRUCES FRIEND
sqlite> SELECT * FROM people WHERE phone_number = '(375) 555-8161';
+--------+-------+----------------+-----------------+---------------+
|   id   | name  |  phone_number  | passport_number | license_plate |
+--------+-------+----------------+-----------------+---------------+
| 864400 | Robin | (375) 555-8161 |                 | 4V16VO0       |
+--------+-------+----------------+-----------------+---------------+

sqlite> SELECT * FROM flights JOIN airports ON airports.id = flights.destination_airport_id WHERE destination_airport_id = '4';
+----+-------------------+------------------------+------+-------+-----+------+--------+----+--------------+-------------------+---------------+
| id | origin_airport_id | destination_airport_id | year | month | day | hour | minute | id | abbreviation |     full_name     |     city      |
+----+-------------------+------------------------+------+-------+-----+------+--------+----+--------------+-------------------+---------------+
| 10 | 8                 | 4                      | 2021 | 7     | 30  | 13   | 55     | 4  | LGA          | LaGuardia Airport | New York City |
| 17 | 8                 | 4                      | 2021 | 7     | 28  | 20   | 16     | 4  | LGA          | LaGuardia Airport | New York City |
| 35 | 8                 | 4                      | 2021 | 7     | 28  | 16   | 16     | 4  | LGA          | LaGuardia Airport | New York City |
| 36 | 8                 | 4                      | 2021 | 7     | 29  | 8    | 20     | 4  | LGA          | LaGuardia Airport | New York City |
| 55 | 8                 | 4                      | 2021 | 7     | 26  | 21   | 44     | 4  | LGA          | LaGuardia Airport | New York City |
+----+-------------------+------------------------+------+-------+-----+------+--------+----+--------------+-------------------+---------------+








