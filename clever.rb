# Clever Tind - Dating with cleverbot
# Like everyone, download profiles, start and hold conversations!
# Dan Kolbman 2014

require 'json'
require 'pyro.rb'
require 'watir-webdriver'
require 'fileutils'
require 'cleverbot'
require 'time'

# fb_auth.rb holds four variables that need to be defined:
# $myLogin - the facebook e-mail address for the fb account with tinder
# $myPasswork - the password the fb account
# fb_id - the fb id number of the account
load 'fb_auth.rb', true

# this will be assigned later, needed to authenticate with tinder
$fb_token = ''

# Need to remember the last time of update so we don't keep request the whole log
$last_update = Time.now - 3000000 #  172800

# Likes all users
def likeEveryone(pyro, bot)
  liked = 0
  rng = Random.new
  
  begin
    begin
      puts "Fetching reccomendations..."
      # Get some users
      recs = pyro.get_nearby_users
      profiles = recs["results"]

      if rng.rand(100) > 0 then
        puts "Checking for updates"
        update(pyro, bot)
      end
      
      while (recs["message"] == "recs timeout" or !profiles)
        # Update and wait until users are available
        puts "Checking for updates"
        update(pyro, bot)
        sleep(30)
        recs = pyro.get_nearby_users
        profiles = recs["results"]
      end


      # Iterate each profile
      for p in profiles
        puts "Liking "+p["name"]

        # User id
        id = p["_id"]
        FileUtils::mkdir_p 'profiles/'+id

        puts "id: "+id

        File.open("log.txt", 'a') do |f|
        f.write("Liking #{p["name"]}\n")
        f.write("#{p["_id"]}\n")
        end

        # Save picture
        begin
          File.open("profiles/"+id+"/"+p["photos"][0]["fileName"], "wb") do |f| 
          f.write HTTParty.get(p["photos"][0]["processedFiles"][0]["url"]).parsed_response
        end
        rescue Exception => msg
          puts "Couldn't retrieve picture"
        end

        File.open("profiles/"+id+"/profile.json", 'w') do |f|
        f.write(p)
      end

      # Like her!
      pyro.like(id)
      liked += 1

    end

    puts "Like #{liked} profiles so far!!!"
    #puts "UPDATES"
    #puts pyro.fetch_updates
        
    rescue Exception => msg
      puts "Error!!!!"
      puts msg
      sleep(300)
    end

  end while (recs["status"] == 200)
end

# Update and respond to messages
def update(pyro, bot)
  rng = Random.new
  msgs = Array["You're the best, ", "I think I love you, ", "I like turtles and I
    like ", "Will you marry me, ", "Mmm my shell is so hard for you ", "Can you
    wax my shell,"]
  
  # Fetch updates from two days ago
  updates = pyro.fetch_updates($last_update)
  # remember when we last updated to avoid repeatedly fetching the same updates
  $last_update = Time.now-2

  #puts JSON.pretty_generate(updates)

  # We have new messages or new matches
  if updates["matches"] != nil and updates["matches"].length > 0   then
    # Iterate every new match update
    for match in updates["matches"]

      # Check if we have a conversation going
      if match["messages"].length > 0 then

        # Check if the last message was to me
        if match["messages"][-1]["to"] == $me then
          
          # Respond to the last message
          # We don't get anything but the user's id for existing conversations
          user_name  = pyro.info_for_user(match["messages"][-1]["from"])
          puts user_name.body.length
          # Check that user still exists
          if user_name.body.length != 0 && user_name["status"] != "500" then
            user_name = user_name["results"]["name"]
            puts "--- #{user_name} said:"
            message = match["messages"][-1]["message"]
            puts "\"#{message}\""
            # Think of a response
            puts "-- Cleverbot responded:"
            reply = cleverResponse(bot, message)
            pyro.send_message(match["_id"], reply)      
            puts "\"#{reply}\""
          end

        end

      else # Start a new conversation
        # We get the person's profile if we haven't sent them any messages
        user_name = match["person"]["name"]
        puts user_name
        puts "--- Starting a conversation with "+user_name
        puts "-- Cleverbot said:"
        reply = "#{msgs[rng.rand(msgs.length)]}#{user_name}!"
        if rng.rand(100) > 90 then # Seed the bot on the user's name
          reply = cleverResponse(bot, user_name)
        end
        puts "\"#{reply}\""
        pyro.send_message(match["_id"], reply)      
      
      end
      
    end
  end

  puts "No more updates"
    
end

def revive(pyro, bot)
  # Fetch updates from two days ago
  updates = pyro.fetch_updates($last_update)
  # remember when we last updated to avoid repeatedly fetching the same updates
  $last_update = Time.now-2
  
  if updates["matches"] != nil and updates["matches"].length > 0   then
    # Iterate every new match update
    for match in updates["matches"]

      # Check if we have a conversation going
      if match["messages"] != nil && match["messages"].length > 1 then
        sent_time = (match["messages"][-1]["timestamp"]/1000).round
        tdiff = Time.now.to_i - sent_time
        if( tdiff > 36 )

          puts "--- Reviving conversation with #{match["person"]["name"]}"
          puts "-- Cleverbot said:"
          reply = cleverResponse(bot, match["messages"][-1]["message"])
          puts "\"#{reply}\""
          pyro.send_message(match["_id"], reply)      
          
        end
      end

    end
  end
end

# Have the bot come up with a response and make sure to filter it
def cleverResponse(bot, message)
  # Think of a response
  valid_reply = false
  while( !valid_reply )
    reply = bot.write message
    # The server is denying us
    if /html/i.match(reply) != nil
      puts "!!!!!! the server won't let us interact with cleverbot. 5min timeout"
      sleep(300)
    # Check for ads
    elsif (/Clev/i.match(reply) != nil or /ios/i.match(reply) != nil)
      puts "!!!!!! Cleverbot gave an ad:" + reply
    else
      valid_reply = true
    end
 end
  return reply
end

# Chat with a match
# Loads profile ids from a folder
def getProfiles(path)
  # Get folder names
  folders = Dir.glob(path+'/*').select {|f| File.directory? f}
  profiles = []
  # Get id from name
  for folder in folders
    # Get ids from paths
    id = /[0-9a-f]{5,30}$/.match(folder)
    profiles.push(id[0])
  end
  return profiles
end



################################################################################
# Actual stuff

puts '====== CLEVER TINDER ======'

# Log us in
if($fb_token == '')
  puts '--- FACEBOOK ---'
  puts 'Fetching Facebook data...'
  # Fetching your Facebook Tinder token & id
  browser = Watir::Browser.new
  puts 'Fetching your Facebook Tinder token...'
  browser.goto 'https://www.facebook.com/dialog/oauth?client_id=464891386855067&redirect_uri=https://www.facebook.com/connect/login_success.html&scope=basic_info,email,public_profile,user_about_me,user_activities,user_birthday,user_education_history,user_friends,user_interests,user_likes,user_location,user_photos,user_relationship_details&response_type=token'
  browser.text_field(:id => 'email').when_present.set $myLogin
  browser.text_field(:id => 'pass').when_present.set $myPassword
  browser.button(:name => 'login').when_present.click

  puts 'Fetching your Facebook ID...'
  $fb_token = /#access_token=(.*)&expires_in/.match(browser.url).captures[0]
  puts "FB_TOKEN:\n"+$fb_token

  puts "FB_ID:\n"+$fb_id

  browser.close
end

pyro = TinderPyro::Client.new
# Get my Tinder ID
$me = pyro.sign_in($fb_id, $fb_token)["user"]["_id"]

# New York
latitude = 40.7198
longitude = -73.9727

pyro.update_location(latitude, longitude)

# Make a bot to chat with
bot = Cleverbot::Client.new

#chat(pyro)
#updateConvos(pyro, bot)

#exit

### Find who matched with us
puts "--- Update conversations ---"
update(pyro, bot)

#scanMatches(pyro)

# Like everyone!!!
puts "--- Liking Everyone! ---"
likeEveryone(pyro, bot)

