-- Keep a log of any SQL queries you execute as you solve the mystery.

-- 1. Review the crime scene reports data
SELECT * FROM crime_scene_reports;
-- 1.a Keep relevant fields only. All reports are from 2021...
SELECT month, day, street, description
  FROM crime_scene_reports
 WHERE month = 7
   AND day > 25;
-- The crime took place on July 28, 2021. No other reports seem to be relevant
-- read record: TIME 10:15 am
-- 1.b Search for more mentions of the bakery
SELECT month, day, street, description
  FROM crime_scene_reports
 WHERE description LIKE '%bakery%';

-- 2. Review interview data from the same date with mentions of the bakery (3 records expected). Other interviews seem irrelevant
SELECT id, name, transcript
  FROM interviews
 WHERE month = 7
   AND day = 28
   AND transcript LIKE '%bakery%';
/* The thief withdrow some money from the ATM of Leggett Street earlier -> 3
   The thief made a call while leaving for LESS THAN A MINUTE asking to purchase the FIRST flight out of Fiftyville next day -> 4
   The thief drove away from the bakery parking lot within 10 min of the crime -> 5 */

-- 3. Check ATM transactions from Leggett Street same day
SELECT account_number, amount
  FROM atm_transactions
 WHERE atm_location = 'Leggett Street'
   AND month = 7
   AND day = 28
   AND transaction_type = 'withdraw';
-- 3.a Obtain a SUSPECT LIST from here
CREATE TABLE SuspectsList AS
SELECT name
  FROM people AS p
       JOIN bank_accounts AS b
       ON b.person_id = p.id
 WHERE account_number IN
       (SELECT account_number
          FROM atm_transactions
         WHERE atm_location = 'Leggett Street'
           AND month = 7
           AND day = 28
           AND transaction_type = 'withdraw');

-- 4. Check for suspects who made phone calls the same day.
-- Add receivers name
SELECT p1.name, duration, p2.name
  FROM phone_calls AS pc
       JOIN people AS p1
       ON p1.phone_number = pc.caller
       JOIN people AS p2
       ON p2.phone_number = pc.receiver
 WHERE month = 7
   AND day = 28
   AND p1.name IN (SELECT name FROM SuspectsList);
-- 4.a Discard suspects who didnt make SHORT calls that day, with set-difference (EXCEPT)
SELECT * FROM SuspectsList
EXCEPT
SELECT name
  FROM people AS p
       JOIN phone_calls AS pc
       ON p.phone_number = pc.caller
 WHERE month = 7
   AND day = 28
   AND duration < 200;
-- This discards Iman, Luca and Brooke

-- 5. Look into plates of cars leaving the parking lot within 15 min (doubting from the 10 min estimation...)
SELECT hour, minute, name
  FROM bakery_security_logs
       JOIN people
       USING (license_plate)
 WHERE month = 7
   AND day = 28
   AND hour = 10
   AND minute BETWEEN 15 and 30
   AND activity ='exit'
ORDER BY hour, minute;
-- 5.a Match the licence plates to list of suspects
SELECT * FROM SuspectsList
INTERSECT
SELECT name
  FROM bakery_security_logs
       JOIN people
       USING (license_plate)
 WHERE month = 7
   AND day = 28
   AND hour = 10
   AND minute BETWEEN 15 and 30
   AND activity ='exit';
-- This keeps Bruce and Diana as FINAL SUSPECTS

-- 6. Look for suspects in flights
-- 6.a Review airports to spot Fiftiville's
SELECT * FROM airports;
-- 6.b Make an insightfull table with flights from Fiftyville NEXT DAY
SELECT hour, minute,
       f.id AS flight, a2.city AS destination,
       CASE WHEN name IN -- Only include passenger name if it's suspect
                 (SELECT name FROM SuspectsList)
                 THEN name
       ELSE 'NS' END AS Suspect
  FROM flights AS f
       JOIN airports AS a1
       ON f.origin_airport_id = a1.id
       JOIN airports AS a2
       ON f.destination_airport_id = a2.id
       JOIN passengers
       ON f.id = flight_id
       JOIN people
       USING (passport_number)
 WHERE a1.city = 'Fiftyville'
   AND month = 7
   AND day = 29
 ORDER BY hour, minute;
 -- BRUCE was on the FIRST plane off Fiftyville
 -- Hence, Bruce is the theft and he flew to NY!!!

 -- 7 look back to query 4 and look for Bruce's calls with duration < 1 min
 -- The reciever (acomplice) is Robin!