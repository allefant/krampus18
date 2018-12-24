from flask import session, escape, request, redirect, url_for
import random
import database
import krampus18

def do_login():
    username = request.form["username"]
    access_phrase = request.form["access_phrase"]
    database.access_db()
    result = database.login(username, access_phrase)
    if result in ["new", "login"]:
        session['username'] = username
        session["result"] = result
        return redirect(url_for("main"))

    h = krampus18.init()
    with h.tag("html"):
        krampus18.header()
        with h.tag("body"):
            with h.tag("h1"):
                h.content("Could not login " + username + ".")
                h.tag2("br")
            if result == "phrase":
                h.content("The access phrase did not match.")
            if result == "name":
                h.content("The name was not valid.")
            if result == "error":
                h.content("The database connection failed.")
    with h.tag("p"):
        with h.tag("a", href = "/"):
            h.content("Back")
    return krampus18.get_html()

def get_username(h):
    username = None
    if "username" in session:
        username = escape(session["username"])
        with h.tag("p"):
            if "result" in session:
                if session["result"] == "new":
                    h.content("Welcome " + username + "!")
                else:
                    h.content("Login successful.")
                h.tag2("br")
                session.pop("result", None)
            h.content("Found session cookie for " + username + ".")
            with h.tag("a", href = "/logout"):
                h.content("Logout.")
    else:
        h.content("No session cookie found.")
        with h.tag("form", method = "post", action = "/login"):
            with h.tag("p"):
                with h.tag("b"):
                    h.content("Player Name:")
                h.tag2("input", type = "text", name = "username", value = "unnamed")
                h.tag2("br")
                h.content("Pick a name and share it so others can join your game.")
            with h.tag("p"):
                access_phrase = random.choice(adjectives) + " " + random.choice(animals)
                with h.tag("b"):
                    h.content("Access Phrase:")
                h.tag2("input", type = "text", name = "access_phrase", value = access_phrase)
                h.tag2("br")
                h.content("This is not a password (it is emailed to me in clear text), but once your browser session expires you need to remember it to log back in, or ask me to look it up for you. Yes, I am not a web dev and this entire game is coded from scratch, in C, using no libraries at all.")
            with h.tag("p"):
                h.tag2("input", type = "submit", value = "Login")
    return username

animals = """
Aardvark
Abyssinian
Adelie Penguin
Affenpinscher
Afghan Hound
African Bush Elephant
African Civet
African Clawed Frog
African Forest Elephant
African Palm Civet
African Penguin
African Tree Toad
African Wild Dog
Ainu Dog
Airedale Terrier
Akbash
Akita
Alaskan Malamute
Albatross
Aldabra Giant Tortoise
Alligator
Alpine Dachsbracke
American Bulldog
American Cocker Spaniel
American Coonhound
American Eskimo Dog
American Foxhound
American Pit Bull Terrier
American Staffordshire Terrier
American Water Spaniel
Anatolian Shepherd Dog
Angelfish
Ant
Anteater
Antelope
Appenzeller Dog
Arctic Fox
Arctic Hare
Arctic Wolf
Armadillo
Asian Elephant
Asian Giant Hornet
Asian Palm Civet
Asiatic Black Bear
Australian Cattle Dog
Australian Kelpie Dog
Australian Mist
Australian Shepherd
Australian Terrier
Avocet
Axolotl
Aye Aye 
Baboon
Bactrian Camel
Badger
Balinese
Banded Palm Civet
Bandicoot
Barb
Barn Owl
Barnacle
Barracuda
Basenji Dog
Basking Shark
Basset Hound
Bat
Bavarian Mountain Hound
Beagle
Bear
Bearded Collie
Bearded Dragon
Beaver
Bedlington Terrier
Beetle
Bengal Tiger
Bernese Mountain Dog
Bichon Frise
Binturong
Bird
Birds Of Paradise
Birman
Bison
Black Bear
Black Rhinoceros
Black Russian Terrier
Black Widow Spider
Bloodhound
Blue Lacy Dog
Blue Whale
Bluetick Coonhound
Bobcat
Bolognese Dog
Bombay
Bongo
Bonobo
Booby
Border Collie
Border Terrier
Bornean Orang-utan
Borneo Elephant
Boston Terrier
Bottle Nosed Dolphin
Boxer Dog
Boykin Spaniel
Brazilian Terrier
Brown Bear
Budgerigar
Buffalo
Bull Mastiff
Bull Shark
Bull Terrier
Bulldog
Bullfrog
Bumble Bee
Burmese
Burrowing Frog
Butterfly
Butterfly Fish
Caiman
Caiman Lizard
Cairn Terrier
Camel
Canaan Dog
Capybara
Caracal
Carolina Dog
Cassowary
Cat
Caterpillar
Catfish
Cavalier King Charles Spaniel
Centipede
Cesky Fousek
Chameleon
Chamois
Cheetah
Chesapeake Bay Retriever
Chicken
Chihuahua
Chimpanzee
Chinchilla
Chinese Crested Dog
Chinook
Chinstrap Penguin
Chipmunk
Chow Chow
Cichlid
Clouded Leopard
Clown Fish
Clumber Spaniel
Coati
Cockroach
Collared Peccary
Collie
Common Buzzard
Common Frog
Common Loon
Common Toad
Coral
Cottontop Tamarin
Cougar
Cow
Coyote
Crab
Crab-Eating Macaque
Crane
Crested Penguin
Crocodile
Cross River Gorilla
Curly Coated Retriever
Cuscus
Cuttlefish
Dachshund
Dalmatian
Darwin's Frog
Deer
Desert Tortoise
Deutsche Bracke
Dhole
Dingo
Discus
Doberman Pinscher
Dodo
Dog
Dogo Argentino
Dogue De Bordeaux
Dolphin
Donkey
Dormouse
Dragonfly
Drever
Duck
Dugong
Dunker
Dusky Dolphin
Dwarf Crocodile
Eagle
Earwig
Eastern Gorilla
Eastern Lowland Gorilla
Echidna
Edible Frog
Egyptian Mau
Electric Eel
Elephant
Elephant Seal
Elephant Shrew
Emperor Penguin
Emperor Tamarin
Emu
English Cocker Spaniel
English Shepherd
English Springer Spaniel
Entlebucher Mountain Dog
Epagneul Pont Audemer
Eskimo Dog
Estrela Mountain Dog
Falcon
Fennec Fox
Ferret
Field Spaniel
Fin Whale
Finnish Spitz
Fire-Bellied Toad
Fish
Fishing Cat
Flamingo
Flat Coat Retriever
Flounder
Fly
Flying Squirrel
Fossa
Fox
Fox Terrier
French Bulldog
Frigatebird
Frilled Lizard
Frog
Fur Seal
Galapagos Penguin
Galapagos Tortoise
Gar
Gecko
Gentoo Penguin
Geoffroys Tamarin
Gerbil
German Pinscher
German Shepherd
Gharial
Giant African Land Snail
Giant Clam
Giant Panda Bear
Giant Schnauzer
Gibbon
Gila Monster
Giraffe
Glass Lizard
Glow Worm
Goat
Golden Lion Tamarin
Golden Oriole
Golden Retriever
Goose
Gopher
Gorilla
Grasshopper
Great Dane
Great White Shark
Greater Swiss Mountain Dog
Green Bee-Eater
Greenland Dog
Grey Mouse Lemur
Grey Reef Shark
Grey Seal
Greyhound
Grizzly Bear
Grouse
Guinea Fowl
Guinea Pig
Guppy
Hammerhead Shark
Hamster
Hare
Harrier
Havanese
Hedgehog
Hercules Beetle
Hermit Crab
Heron
Highland Cattle
Himalayan
Hippopotamus
Honey Bee
Horn Shark
Horned Frog
Horse
Horseshoe Crab
Howler Monkey
Human
Humboldt Penguin
Hummingbird
Humpback Whale
Hyena
Ibis
Ibizan Hound
Iguana
Impala
Indian Elephant
Indian Palm Squirrel
Indian Rhinoceros
Indian Star Tortoise
Indochinese Tiger
Indri
Insect
Irish Setter
Irish WolfHound
Jack Russel
Jackal
Jaguar
Japanese Chin
Japanese Macaque
Javan Rhinoceros
Javanese
Jellyfish
Kakapo
Kangaroo
Keel Billed Toucan
Killer Whale
King Crab
King Penguin
Kingfisher
Kiwi
Koala
Komodo Dragon
Kudu
Labradoodle
Labrador Retriever
Ladybird
Leaf-Tailed Gecko
Lemming
Lemur
Leopard
Leopard Cat
Leopard Seal
Leopard Tortoise
Liger
Lion
Lionfish
Little Penguin
Lizard
Llama
Lobster
Long-Eared Owl
Lynx
Macaroni Penguin
Macaw
Magellanic Penguin
Magpie
Maine Coon
Malayan Civet
Malayan Tiger
Maltese
Manatee
Mandrill
Manta Ray
Marine Toad
Markhor
Marsh Frog
Masked Palm Civet
Mastiff
Mayfly
Meerkat
Millipede
Minke Whale
Mole
Molly
Mongoose
Mongrel
Monitor Lizard
Monkey
Monte Iberia Eleuth
Moorhen
Moose
Moray Eel
Moth
Mountain Gorilla
Mountain Lion
Mouse
Mule
Neanderthal
Neapolitan Mastiff
Newfoundland
Newt
Nightingale
Norfolk Terrier
Norwegian Forest
Numbat
Nurse Shark
Ocelot
Octopus
Okapi
Old English Sheepdog
Olm
Opossum
Orang-utan
Ostrich
Otter
Oyster
Pademelon
Panther
Parrot
Patas Monkey
Peacock
Pekingese
Pelican
Penguin
Persian
Pheasant
Pied Tamarin
Pig
Pika
Pike
Pink Fairy Armadillo
Piranha
Platypus
Pointer
Poison Dart Frog
Polar Bear
Pond Skater
Poodle
Pool Frog
Porcupine
Possum
Prawn
Proboscis Monkey
Puffer Fish
Puffin
Pug
Puma
Purple Emperor
Puss Moth
Pygmy Hippopotamus
Pygmy Marmoset
Quail
Quetzal
Quokka
Quoll
Rabbit
Raccoon
Raccoon Dog
Radiated Tortoise
Ragdoll
Rat
Rattlesnake
Red Knee Tarantula
Red Panda
Red Wolf
Red-handed Tamarin
Reindeer
Rhinoceros
River Dolphin
River Turtle
Robin
Rock Hyrax
Rockhopper Penguin
Roseate Spoonbill
Rottweiler
Royal Penguin
Russian Blue
Sabre-Toothed Tiger
Saint Bernard
Salamander
Sand Lizard
Saola
Scorpion
Scorpion Fish
Sea Dragon
Sea Lion
Sea Otter
Sea Slug
Sea Squirt
Sea Turtle
Sea Urchin
Seahorse
Seal
Serval
Sheep
Shih Tzu
Shrimp
Siamese
Siamese Fighting Fish
Siberian
Siberian Husky
Siberian Tiger
Silver Dollar
Skunk
Sloth
Slow Worm
Snail
Snake
Snapping Turtle
Snowshoe
Snowy Owl
Somali
South China Tiger
Spadefoot Toad
Sparrow
Spectacled Bear
Sperm Whale
Spider Monkey
Spiny Dogfish
Sponge
Squid
Squirrel
Squirrel Monkey
Sri Lankan Elephant
Staffordshire Bull Terrier
Stag Beetle
Starfish
Stellers Sea Cow
Stick Insect
Stingray
Stoat
Striped Rocket Frog
Sumatran Elephant
Sumatran Orang-utan
Sumatran Rhinoceros
Sumatran Tiger
Sun Bear
Swan
Tang
Tapanuli Orang-utan
Tapir
Tarsier
Tasmanian Devil
Tawny Owl
Termite
Tetra
Thorny Devil
Tibetan Mastiff
Tiffany
Tiger
Tiger Salamander
Tiger Shark
Tortoise
Toucan
Tree Frog
Tropicbird
Tuatara
Turkey
Turkish Angora
Uakari
Uguisu
Umbrellabird
Vampire Bat
Vervet Monkey
Vulture
Wallaby
Walrus
Warthog
Wasp
Water Buffalo
Water Dragon
Water Vole
Weasel
Welsh Corgi
West Highland Terrier
Western Gorilla
Western Lowland Gorilla
Whale Shark
Whippet
White Faced Capuchin
White Rhinoceros
White Tiger
Wild Boar
Wildebeest
Wolf
Wolverine
Wombat
Woodlouse
Woodpecker
Woolly Mammoth
Woolly Monkey
Wrasse
X-Ray Tetra
Yak
Yellow-Eyed Penguin
Yorkshire Terrier
Zebra
Zebra Shark
Zebu
Zonkey
Zorse
""".strip().splitlines()

adjectives = """
abandoned
able
absolute
academic
acceptable
acclaimed
accomplished
accurate
aching
acidic
acrobatic
active
actual
adept
admirable
admired
adolescent
adorable
adored
advanced
adventurous
affectionate
afraid
aged
aggravating
aggressive
agile
agitated
agonizing
agreeable
ajar
alarmed
alarming
alert
alienated
alive
all
altruistic
amazing
ambitious
ample
amused
amusing
anchored
ancient
angelic
angry
anguished
animated
annual
another
antique
anxious
any
apprehensive
appropriate
apt
arctic
arid
aromatic
artistic
ashamed
assured
astonishing
athletic
attached
attentive
attractive
austere
authentic
authorized
automatic
avaricious
average
aware
awesome
awful
awkward
babyish
back
bad
baggy
bare
barren
basic
beautiful
belated
beloved
beneficial
best
better
bewitched
big
big-hearted
biodegradable
bite-sized
bitter
black
black-and-white
bland
blank
blaring
bleak
blind
blissful
blond
blue
blushing
bogus
boiling
bold
bony
boring
bossy
both
bouncy
bountiful
bowed
brave
breakable
brief
bright
brilliant
brisk
broken
bronze
brown
bruised
bubbly
bulky
bumpy
buoyant
burdensome
burly
bustling
busy
buttery
buzzing
calculating
calm
candid
canine
capital
carefree
careful
careless
caring
cautious
cavernous
celebrated
charming
cheap
cheerful
cheery
chief
chilly
chubby
circular
classic
clean
clear
clear-cut
clever
close
closed
cloudy
clueless
clumsy
cluttered
coarse
cold
colorful
colorless
colossal
comfortable
common
compassionate
competent
complete
complex
complicated
composed
concerned
concrete
confused
conscious
considerate
constant
content
conventional
cooked
cool
cooperative
coordinated
corny
corrupt
costly
courageous
courteous
crafty
crazy
creamy
creative
creepy
criminal
crisp
critical
crooked
crowded
cruel
crushing
cuddly
cultivated
cultured
cumbersome
curly
curvy
cute
cylindrical
damaged
damp
dangerous
dapper
daring
dark
darling
dazzling
dead
deadly
deafening
dear
dearest
decent
decimal
decisive
deep
defenseless
defensive
defiant
deficient
definite
definitive
delayed
delectable
delicious
delightful
delirious
demanding
dense
dental
dependable
dependent
descriptive
deserted
detailed
determined
devoted
different
difficult
digital
diligent
dim
dimpled
dimwitted
direct
dirty
disastrous
discrete
disfigured
disguised
disgusting
dishonest
disloyal
dismal
distant
distinct
distorted
dizzy
dopey
doting
double
downright
drab
drafty
dramatic
dreary
droopy
dry
dual
dull
dutiful
each
eager
early
earnest
easy
easy-going
ecstatic
edible
educated
elaborate
elastic
elated
elderly
electric
elegant
elementary
elliptical
embarrassed
embellished
eminent
emotional
empty
enchanted
enchanting
energetic
enlightened
enormous
enraged
entire
envious
equal
equatorial
essential
esteemed
ethical
euphoric
even
evergreen
everlasting
every
evil
exalted
excellent
excitable
excited
exciting
exemplary
exhausted
exotic
expensive
experienced
expert
extra-large
extra-small
extraneous
extroverted
fabulous
failing
faint
fair
faithful
fake
false
familiar
famous
fancy
fantastic
far
far-flung
far-off
faraway
fast
fat
fatal
fatherly
favorable
favorite
fearful
fearless
feisty
feline
female
feminine
few
fickle
filthy
fine
finished
firm
first
firsthand
fitting
fixed
flaky
flamboyant
flashy
flat
flawed
flawless
flickering
flimsy
flippant
flowery
fluffy
fluid
flustered
focused
fond
foolhardy
foolish
forceful
forked
formal
forsaken
forthright
fortunate
fragrant
frail
frank
frayed
free
French
frequent
fresh
friendly
frightened
frightening
frigid
frilly
frivolous
frizzy
front
frosty
frozen
frugal
fruitful
full
fumbling
functional
funny
fussy
fuzzy
gargantuan
gaseous
general
generous
gentle
genuine
giant
giddy
gifted
gigantic
giving
glamorous
glaring
glass
gleaming
gleeful
glistening
glittering
gloomy
glorious
glossy
glum
golden
good
good-natured
gorgeous
graceful
gracious
grand
grandiose
granular
grateful
grave
gray
great
greedy
green
gregarious
grim
grimy
gripping
grizzled
gross
grotesque
grouchy
grounded
growing
growling
grown
grubby
gruesome
grumpy
guilty
gullible
gummy
hairy
half
handmade
handsome
handy
happy
happy-go-lucky
hard
hard-to-find
harmful
harmless
harmonious
harsh
hasty
hateful
haunting
healthy
heartfelt
hearty
heavenly
heavy
hefty
helpful
helpless
hidden
hideous
high
high-level
hilarious
hoarse
hollow
homely
honest
honorable
honored
hopeful
horrible
hospitable
hot
huge
humble
humiliating
humming
humongous
hungry
hurtful
husky
icky
icy
ideal
idealistic
identical
idiotic
idle
idolized
ignorant
ill
ill-fated
ill-informed
illegal
illiterate
illustrious
imaginary
imaginative
immaculate
immaterial
immediate
immense
impartial
impassioned
impeccable
imperfect
imperturbable
impish
impolite
important
impossible
impractical
impressionable
impressive
improbable
impure
inborn
incomparable
incompatible
incomplete
inconsequential
incredible
indelible
indolent
inexperienced
infamous
infantile
infatuated
inferior
infinite
informal
innocent
insecure
insidious
insignificant
insistent
instructive
insubstantial
intelligent
intent
intentional
interesting
internal
international
intrepid
ironclad
irresponsible
irritating
itchy
jaded
jagged
jam-packed
jaunty
jealous
jittery
joint
jolly
jovial
joyful
joyous
jubilant
judicious
juicy
jumbo
jumpy
junior
juvenile
kaleidoscopic
keen
key
kind
kindhearted
kindly
klutzy
knobby
knotty
knowing
knowledgeable
known
kooky
kosher
lame
lanky
large
last
lasting
late
lavish
lawful
lazy
leading
leafy
lean
left
legal
legitimate
light
lighthearted
likable
likely
limited
limp
limping
linear
lined
liquid
little
live
lively
livid
loathsome
lone
lonely
long
long-term
loose
lopsided
lost
loud
lovable
lovely
loving
low
loyal
lucky
lumbering
luminous
lumpy
lustrous
luxurious
mad
made-up
magnificent
majestic
major
male
mammoth
married
marvelous
masculine
massive
mature
meager
mealy
mean
measly
meaty
medical
mediocre
medium
meek
mellow
melodic
memorable
menacing
merry
messy
metallic
mild
milky
mindless
miniature
minor
minty
miserable
miserly
misguided
misty
mixed
modern
modest
moist
monstrous
monthly
monumental
moral
mortified
motherly
motionless
mountainous
muddy
muffled
multicolored
mundane
murky
mushy
musty
muted
mysterious
naive
narrow
nasty
natural
naughty
nautical
near
neat
necessary
needy
negative
neglected
negligible
neighboring
nervous
new
next
nice
nifty
nimble
nippy
nocturnal
noisy
nonstop
normal
notable
noted
noteworthy
novel
noxious
numb
nutritious
nutty
obedient
obese
oblong
obvious
occasional
odd
oddball
offbeat
offensive
official
oily
old
old-fashioned
only
open
optimal
optimistic
opulent
orange
orderly
ordinary
organic
original
ornate
ornery
other
our
outgoing
outlandish
outlying
outrageous
outstanding
oval
overcooked
overdue
overjoyed
overlooked
palatable
pale
paltry
parallel
parched
partial
passionate
past
pastel
peaceful
peppery
perfect
perfumed
periodic
perky
personal
pertinent
pesky
pessimistic
petty
phony
physical
piercing
pink
pitiful
plain
plaintive
plastic
playful
pleasant
pleased
pleasing
plump
plush
pointed
pointless
poised
polished
polite
political
poor
popular
portly
posh
positive
possible
potable
powerful
powerless
practical
precious
present
prestigious
pretty
previous
pricey
prickly
primary
prime
pristine
private
prize
probable
productive
profitable
profuse
proper
proud
prudent
punctual
pungent
puny
pure
purple
pushy
putrid
puzzled
puzzling
quaint
qualified
quarrelsome
quarterly
queasy
querulous
questionable
quick
quick-witted
quiet
quintessential
quirky
quixotic
quizzical
radiant
ragged
rapid
rare
rash
raw
ready
real
realistic
reasonable
recent
reckless
rectangular
red
reflecting
regal
regular
reliable
relieved
remarkable
remorseful
remote
repentant
repulsive
required
respectful
responsible
revolving
rewarding
rich
right
rigid
ringed
ripe
roasted
robust
rosy
rotating
rotten
rough
round
rowdy
royal
rubbery
ruddy
rude
rundown
runny
rural
rusty
sad
safe
salty
same
sandy
sane
sarcastic
sardonic
satisfied
scaly
scarce
scared
scary
scented
scholarly
scientific
scornful
scratchy
scrawny
second
second-hand
secondary
secret
self-assured
self-reliant
selfish
sentimental
separate
serene
serious
serpentine
several
severe
shabby
shadowy
shady
shallow
shameful
shameless
sharp
shimmering
shiny
shocked
shocking
shoddy
short
short-term
showy
shrill
shy
sick
silent
silky
silly
silver
similar
simple
simplistic
sinful
single
sizzling
skeletal
skinny
sleepy
slight
slim
slimy
slippery
slow
slushy
small
smart
smoggy
smooth
smug
snappy
snarling
sneaky
sniveling
snoopy
sociable
soft
soggy
solid
somber
some
sophisticated
sore
sorrowful
soulful
soupy
sour
Spanish
sparkling
sparse
specific
spectacular
speedy
spherical
spicy
spiffy
spirited
spiteful
splendid
spotless
spotted
spry
square
squeaky
squiggly
stable
staid
stained
stale
standard
starchy
stark
starry
steel
steep
sticky
stiff
stimulating
stingy
stormy
straight
strange
strict
strident
striking
striped
strong
studious
stunning
stupendous
stupid
sturdy
stylish
subdued
submissive
substantial
subtle
suburban
sudden
sugary
sunny
super
superb
superficial
superior
supportive
sure-footed
surprised
suspicious
svelte
sweaty
sweet
sweltering
swift
sympathetic
talkative
tall
tame
tan
tangible
tart
tasty
tattered
taut
tedious
teeming
tempting
tender
tense
tepid
terrible
terrific
testy
thankful
that
these
thick
thin
third
thirsty
this
thorny
thorough
those
thoughtful
threadbare
thrifty
thunderous
tidy
tight
timely
tinted
tiny
tired
torn
total
tough
tragic
trained
traumatic
treasured
tremendous
triangular
tricky
trifling
trim
trivial
troubled
true
trusting
trustworthy
trusty
truthful
tubby
turbulent
twin
ugly
ultimate
unacceptable
unaware
uncomfortable
uncommon
unconscious
understated
unequaled
uneven
unfinished
unfit
unfolded
unfortunate
unhappy
unhealthy
uniform
unimportant
unique
united
unkempt
unknown
unlawful
unlined
unlucky
unnatural
unpleasant
unrealistic
unripe
unruly
unselfish
unsightly
unsteady
unsung
untidy
untimely
untried
untrue
unused
unusual
unwelcome
unwieldy
unwilling
unwitting
unwritten
upbeat
upright
upset
urban
usable
used
useful
useless
utilized
utter
vacant
vague
vain
valid
valuable
vapid
variable
vast
velvety
venerated
vengeful
verifiable
vibrant
vicious
victorious
vigilant
vigorous
villainous
violent
violet
virtual
virtuous
visible
vital
vivacious
vivid
voluminous
wan
warlike
warm
warmhearted
warped
wary
wasteful
watchful
waterlogged
watery
wavy
weak
wealthy
weary
webbed
wee
weekly
weepy
weighty
weird
welcome
well-documented
well-groomed
well-informed
well-lit
well-made
well-off
well-to-do
well-worn
wet
which
whimsical
whirlwind
whispered
white
whole
whopping
wicked
wide
wide-eyed
wiggly
wild
willing
wilted
winding
windy
winged
wiry
wise
witty
wobbly
woeful
wonderful
wooden
woozy
wordy
worldly
worn
worried
worrisome
worse
worst
worthless
worthwhile
worthy
wrathful
wretched
writhing
wrong
wry
yawning
yearly
yellow
yellowish
young
youthful
yummy
zany
zealous
zesty
zigzag
""".strip().splitlines()
