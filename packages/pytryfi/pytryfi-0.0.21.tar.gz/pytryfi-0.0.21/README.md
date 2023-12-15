# pytryfi - Python Interface for TryFi

This python interface enables you to gather information about your dogs whereabouts, your user details and any bases you may have.

NOTE: Since this interacts with undocumented APIs, this may change without notice.

## Installation

To install this package, use pip

```python
python -m pip install "pytryfi"
```

## Usage

TryFi uses Graphql for its APIs. Essentially, you will use your username (email address) and password to retrieve a unique username specific for API calls which in turn will be used for the duration to retrieve data.

### Login Script with Debugging Support

```sh
# Export env variables
export fi_user=user@user.com
export fi_pass=secretpassword

# When running in Dev container, uncomment & use the args in the `launch.json` file for vscode or set manually in your workspace terminal
export fi_user=user@user.com
export fi_pass=secretpassword

# run script in terminal
python login.py

# Alternatively run script in debugger and set breakpoints as needed (recommended to set one on line 31 of login.py for an example)
hit F5 to start the debugger
```

### Manual Example

```python
#this will create the object and gather all the necessary data
tryfi = PyTryFi(username, password)
print(tryfi)

#this will perform a complete refresh of all Pets and data points
tryfi.updatePets()

#this will perform a complete refresh of all Bases and data points
tryfi.updateBases()

#this will perform an update on both Pets and Bases and their associated data points
tryfi.update()

#this will update the last reported location of a bet
tryfi.pets[0].updatePetLocation(tryfi.session)

#this will update the stats of the pet
tryfi.pets[0].updateStats(tryfi.session)

#this will update rest (nap/sleep) stats of the pet
tryfi.pets[0].updateRestStats(tryfi.session)

#update the device/collar details for the given pet
tryfi.pets[0].updateDeviceDetails(tryfi.session)

#update the all details for a given pet
tryfi.pets[0].updateAllDetails(tryfi.session)

#this will set the light color of the collar
tryfi.pets[0].setLedColorCode(tryfi.session, 2)

#this will turn on the LED light on the color
tryfi.pets[0].turnOnOffLed(tryfi.session,True)
#or turn it off
tryfi.pets[0].turnOnOffLed(tryfi.session,False)

#this will turn on the lost dog mode
tryfi.pets[0].setLostDogMode(tryfi.session,True)
#or turn it off
tryfi.pets[0].setLostDogMode(tryfi.session,False)

#this will get the lost dog mode status/state currently in the object
tryfi.pets[0].isLost

#this will query sleep stats for given pet
tryfi.pets[0].dailySleep
tryfi.pets[0].weeklySleep
tryfi.pets[0].monthlySleep

#this will query nap stats for given pet
tryfi.pets[0].dailyNap
tryfi.pets[0].weeklyNap
tryfi.pets[0].monthlyNap
```

## To Do

- Provide Activity Data History

## Links:

- [TryFi](https://tryfi.com/)

# Version History

# 0.0.21
- Enchanced error handling of pet information in case its not available

# 0.0.20
- Fix - Added HTTP Header to the requests of all GraphQL requests

# 0.0.19

- Breaking Change - removed battery health as its not available in the newer collars and deprecated
- Fix - If a pet exists and has no collar then ignore. Previously it would attempt to associate a collar that doesn't exist and error out.

# 0.0.18

- Maintenance - Removal of walkversion which is being deprecated and no longer required.

# 0.0.17

- Enhancement - added 3 functions to get the Activity Type, Current Place Name and Current Place Address

# 0.0.16

- Fix - removed hardcoding of a single household. Households are iterated through for pets and bases.

# 0.0.15

- Enhancement - added Sleep and Nap statistics. If the collar doesn't support this feature it defaults to zero.

# 0.0.14

- Fix - resolved issue between V1 and V2 of the TryFi collars where the isCharging property doesn't exist in V2. This causes failed parsing errors and some users get a ledOn error as a symptom in hass-tryfi (Home Assistant - TryFi implementation)

# 0.0.13

- Enhancement - removed error logging where not required
- Fix - resolved issue where the variables are unbound in the login function

## 0.0.12

- Enhancement - added Sentry for capturing errors by further only capturing exceptions

## 0.0.11

- Enhancement - added Sentry for capturing errors

## 0.0.10

- Enhancement - added areaName property that could be used to idenitfy a location (tryfi.pets[0].areaName)
- Bugfix - fixed longitude and latitude while Pet is on a walk

## 0.0.9

- Bugfix - get LED status based on additional logic that compares the ledOffAt date with the current date/time. Update the boolean to True or False base on the additional date comparison.

## 0.0.8

- Bugfix - handle unknown location

## 0.0.7

- Bug fixes when updating objects

## 0.0.6

- Added function to submit Lost Dog Action
- Added isLost property to Pet
- Code cleanup

## 0.0.5

- Added global update function that updates both pets and bases (pytryfi.update())
- Added better error handling

## 0.0.4

- created update functions for various pet and device objects and a global update for the pet
- added last updated date/time to the objects to track when the data was last updated
- changed turn on/off action to boolean
- when performing an action on the collar, update the data that is retrieved at the same time

## 0.0.3

The following updates/enhancements were made:

- moved updated pet location from base object to pet class
- created function to update the stats of the pet
- converted approriate variables to integers, floats and dates
- created function to set the LED color on the collar
- created function to turn on/off LED on a collar

## 0.0.2

Initial version of the TryFi interface that gathered basic information about the pets, collars and bases.
