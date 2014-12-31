# Create a bunch of markdown files for conversations
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

# Get updates from way back
$last_update = Time.now - 50000000

# Tinder id
$me = "5430151e3d3b85840f8716ad"

# Paths for output
$page_path = "site/content/posts/"
$img_path = "site/content/images/"



# Loads profile ids from a folder
# Params:
#   path - the path of the profile data directory
def getProfiles(path)
  # Get folder names (ie user IDs)
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


# Makes a markdown page from a bunch of messages
# Params:
#   pyro - the pyro insnance to interact with tinder
#   msgs - list of messages
#   outpath - the output path of the pages
def makePage(pyro, msgs, outpath)

  user_id = msgs[0]["to"]
  if user_id == $me
    user_id = msgs[0]["from"]
  end
  user_info  = pyro.info_for_user(user_id)
  # Make sure the account still exists
  if user_info.body.length > 0 && user_info["status"] != "500" then
    user_name = user_info["results"]["name"]
    photo = user_info["results"]["photos"][0]
    if !File.exist?($img_path+photo["fileName"]) then
      File.open($img_path+photo["fileName"], "wb") do |f| 
        f.write HTTParty.get(photo["processedFiles"][3]["url"]).parsed_response
      end
    end
    # Make header
    pagestr = ""
    pagestr += "title: #{user_name} (#{msgs.length} messages)\n"
    pagestr += "slug: #{user_id}\n"
    pagestr += "date: #{msgs[-1]["sent_date"]}\n"
    pagestr += "author: Mike the Turtle\n"
    pagestr += "image: #{photo["fileName"]}\n\n\n"

    # Format messages
    for msg in msgs
      pagestr += "(#{msg["sent_date"]}) "
      if msg["from"] == $me
        pagestr += "Mike: "
      else
        pagestr += "#{user_name}: "
      end
      
      pagestr += msg["message"]
      pagestr += "\n\n"
      
    end

    File.open($page_path+user_id+".md", 'w') do |f|
    f.write(pagestr)
    end
  end
  
end


# Gets conversations from matches and generate pages for them
def makePages( pyro )
  # Fetch updates from two days ago
  updates = pyro.fetch_updates($last_update)

  puts "Found #{updates["matches"].length} matches"

  # We have new messages or new matches
  if updates["matches"] != nil and updates["matches"].length > 0   then
    # Iterate every new match update
    for match in updates["matches"]

      # Check if we have a conversation going
      if match["messages"] != nil && match["messages"].length > 1 then
        puts "Making page"
        makePage(pyro, match["messages"])
      end
    end
  end
end






################################################################################
# Actual stuff

## Get profile ids

profs = getProfiles( 'profiles' )

puts "Found #{profs.length} profiles"


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
pyro.sign_in($fb_id, $fb_token)


makePages( pyro )


