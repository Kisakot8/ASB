# ASB
Discord bot for my friends and I to use in our server.

For privacy/security reasons, the token, the path to files and the channel ID's have been taken away.

## **CURRENT FEATURES:**
**GENERAL PURPOSE**
- Shut down the bot without opening console with `.shutdown`
    - Shut down the bot with `.powershutdown` in case normal shutdown doesn't work. _Use only if needed: this does NOT perform any shutdown procedures (e.g. adding quotes)_
- Logs every message to a channel
- Lets owner(s) send messages from the bot with `.send "<message>" <channel_name>`
- Multiple debug commands (`.getguild`,`.getchannels`,`.testquotes`,`.checkformsg <channel_id> <message_id>`)
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

**LOCKDOWN**
- Moderators can lock down channels from @everyone
    - Lock down channel with `.lockdown` (typed in channel to lock)
    - Lock down all channels with `.masslockdown`
    - Unlock channel with `.unlock` (typed in channel to unlock)
    - Unlock all channels with `.massunlock`
        - This command doesn't work

**REPEAT MESSAGE**
- Repeats <message> every <interval> seconds (default = 10)
    - `.repeatmessage <start/stop> <interval> <message>`

**POLLS**
- Run polls on teachers stored in txt files with `.createq`
    - Feature no longer in use

## **WHAT IM WORKING ON:**
- Refactor commands to be slash commands
