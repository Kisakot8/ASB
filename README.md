# ASB
Discord bot for my friends and I to use in our server.

For privacy/security reasons, the token, the path to files and the channel ID's have been taken away.

## **CURRENT FEATURES:**
**GENERAL PURPOSE**
- Shut down the bot without opening console with `.shutdown`
- Logs every message to a channel
- Lets owner(s) send messages from the bot with `.send "<message>" <channel_name>`
- Multiple debug commands (`.getguild`,`.getchannels`,`testquotes`)
- Check bot latency with `.ping`

**QUOTES**
- Adding quotes sent in quote-book to a txt file automatically
    - Manually adds all quotes in quote-book with `.addallquotes` or specified amount with `.addquotes <number>`
    - Adds new quotes automatically upon startup
- Send random quote with `.quote`

**BIRTHDAYS**
- Users can add their birthday with `.setbday <name> <DD> <MM> <YYYY>`
    - Birthday can be edited by running .setbday again
- Users will be pinged on their birthday in a special channel
    - Date is automatically checked upon startup to match any registered dates
    - Avoids multiple pings by checking most recent message (if there's any messages to check)

**POLLS**
- Run polls on teachers stored in txt files with `.createq`
    - Feature no longer in use

## **WHAT IM WORKING ON:**
- Create cosmetic colour roles for users by command
