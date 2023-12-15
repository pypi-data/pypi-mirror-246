import random
# every quote are contained in fuctions
# so to use any persons quote just create an instance and call the name of the function inside the instance in your project after importing it
# inside the function the quotes are arranged in dictionary with unique number as key
# using the random module we pick the quote randomly
# the function to call for quotes are--> mark(),jobs(),bill(),elun(),tesla(),einstein(),science(),hackers(),success(),all()
# to use all the quote at ones call the all() function
# to learn more or contribute check our readme.txt file on github 

#function for Mark zuckerberg's quotes
def mark():
    gen = random.randint(1,50)
    name = " --Mark zuckerberg"
    mark = {
            1:"The biggest risk is not taking any risk",
            2:"The question I ask myself like almost every day is, 'Am I doing the most important thing I could be doing?",
            3:"Move fast and break things. Unless you are breaking stuff, you are not moving fast enough",
            4:"I like making things. I don't like getting my picture taken",
            5:"By giving people the power to share, we're making the world more transparent",
            6:"A squirrel dying in front of your house may be more relevant to your interests right now than people dying in Africa",
            7:"Figuring out what the next big trend is tells us what we should focus on",
            8:"Once you have a product that you are happy with, you the need to centralize things to continue growth",
            9:"Our philosophy is that we care about people first",
            10:"The question isn't, 'What do we want to know about people?', It's, 'What do people want to tell about themselves",
            11:"I think a simple rule of business is, if you do the things that are easier first, then you can actually make a lot of progress.",
            12:"The biggest mistake we made as a company was betting too much on HTML5",
            13:"Founding a company is hard. Most of it isn't smooth. You'll have to make very hard decisions. You have to fire a few people. Therefore, if you don't believe in your mission, giving up is easy. The majority of founders give up. But the best founders don't give up.",
            14:"Our mission is to connect every person in the world. You don't do that by having a service people pay for.",
            15:"When you give everyone a voice and give people power, the system usually ends up in a really good place. So, what we view our role as, is giving people that power.",
            16:"I will only hire someone to work directly for me if I would work for that person. It's a pretty good test.",
            17:"You get a reputation for stability if you are stable for years.",
            18:"My goal was never to make Facebook cool. I am not a cool person.",
            19:"I think Facebook is an online directory for colleges... If I want to get information about you, I just go to TheFacebook, type in your name, and it hopefully pulls up all the information I'd care to know about you.",
            20:"When I was in college I did a lot of stupid things and I don't want to make an excuse for that. Some of the things that people accuse me of are true, some of them aren't. There are pranks, IMs",
            21:"I look at Google and think they have a strong academic culture. Elegant solutions to complex problems",
            22:"I started the site when I was 19. I didn't know much about business back then. Share this Quote",
            23:"A lot of times, I run a thought experiment: 'If I were not at Facebook, what would I be doing to make the world more open?",
            24:"I care about helping to address these problems of social cohesion and understanding what economic problems people think exist.",
            25:"The basis of our partnership strategy and our partnership approach: We build the social technology. They provide the music.",
            26:"The amount of trust and bandwidth that you build up working with someone for five, seven, 10 years? It's just awesome. I care about openness and connectedness in a global sense.",
            27:"The real story of Facebook is just that we've worked so hard for all this time. I mean, the real story is actually probably pretty boring, right? I mean, we just sat at our computers for six years and coded.",
            28:"Move fast with stable infrastructure.",
            29:"Our goal is to make it so there's as little friction as possible to having a social experience",
            30:"my number one piece of advice is learn to program",
            31:"I made so many mistakes in running the company so far, basically any mistake you can think of I probably made. I think, if anything, the Facebook story is a great example of how if you're building a product that people love you can make a lot of mistakes",
            32:"I made so many mistakes in running the company so far, basically any mistake you can think of I probably made. I think, if anything, the Facebook story is a great example of how if you're building a product that people love you can make a lot of mistakes",
            33:"We Don't Build Services to Make Money, We Make Money To Build Services.",
            34:"If you just work on stuff that you like and you're passionate about, you don't have to have a master plan with how things will play out.",
            35:"We don't crash EVER!",
            36:"The greatest successes come from having the freedom to fail",
            37:"Your ability to keep doing interesting things is your willingness to be embarrassed and go back to step 1.",
            38:"They just can't wrap their head around the idea that someone might build something because they like building things.",
            39:"Finding your purpose isn't enough. the challenge for our generation is creating a world where everyone has a sense of purpose.",
            40:"I really want to clear my life to make it so that I have to make as few decisions as possible about anything except how to best serve this community",
            41:"Having two identities for yourself is an example of a lack of integrity.",
            42:"People don't care about what you say, they care about what you build.",
            43:"Hire people who believe in your mission, vision, and values",
            44:"Market your stuff based on what people want, not what you need",
            45:"Build a business people will believe in",
            46:"Hire people who are passionate",
            47:"Challenge yourself if you want to succeed",
            48:"Try new stuff, learn from your mistakes, and move on",
            49:"Focus on priorities",
            50:"The biggest risk is not taking any risk in a world that is changing really quickly, the only strategy that is guaranteed to fail is not taking risks."
           }
    return(mark[gen] + name)

#function for steve jobs quote
def jobs():
    gen = random.randint(1,35)
    name = " --Steve jobs"
    jobs = {
           1:"Innovation distinguishes between a leader and a follower.",
           2:"Your time is limited, so don't waste it living someone else's life.",
           3:"Don't let the noise of others' opinions drown out your own inner voice.",
           4:"You can't connect the dots looking forward; you can only connect them looking backwards. So you have to trust that the dots will somehow connect in your future.",
           5:"Stay hungry. Stay foolish",
           6:"You can't just ask customers what they want and then try to give that to them. By the time you get it built, they'll want something new.You can't just ask customers what they want and then try to give that to them. By the time you get it built, they'll want something new.",
           7:"You can't just ask customers what they want and then try to give that to them. By the time you get it built, they'll want something new.",
           8:"We're here to put a dent in the universe. Otherwise why else even be here?",
           9:"The people who are crazy enough to think they can change the world are the ones who do.",
           10:"For the past 33 years, I have looked in the mirror every morning and asked myself: If today were the last day of my life, would I want to do what I am about to do today? And whenever the answer has been No for too many days in a row, I know I need to change something.",
           11:"Your work is going to fill a large part of your life, and the only way to be truly satisfied is to do what you believe is great work. And the only way to do great work is to love what you do. If you haven't found it yet, keep looking. Don't settle. As with all matters of the heart, you'll know when you find it.",
           12:"I've always been attracted to the more revolutionary changes. I don't know why. Because they're harder. They're much more stressful emotionally. And you usually go through a period where everybody tells you that you've completely failed.",
           13:"Be a yardstick of quality. Some people aren't used to an environment where excellence is expected.",
           14:"Quality is more important than quantity. One home run is much better than two doubles.",
           15:"Have the courage to follow your heart and intuition. They somehow already know what you truly want to become. Everything else is secondary",
           16:"Sometimes life's going to hit you in the head with a brick. Don't lose faith. I'm convinced that the only thing that kept me going was that I loved what I did.",
           17:"Why join the navy if you can be a pirate?",
           18:"The only way to do great work is to love what you do. If you haven't found it yet, keep looking. Don't settle.",
           19:"The heaviness of being successful was replaced by the lightness of being a beginner again.",
           20:"People who know what they are talking about don't need power Point.",
           21:" had no idea what I wanted to do with my life and no idea how college was going to help me figure it out.",
           22:"If you don't love something, you're not going to go the extra mile, work the extra weekend, challenge the status quo as much",
           23:"I keep thinking about all the time away from my family this will cause, and the time away from my other family at Pixar, but the only reason I want to do it is that the world will be a better place with Apple in it.",
           24:" Being the richest man in the cemetery doesn't matter to me … Going to bed at night saying we've done something wonderful … that's what matters to me.",
           25:"I've been rejected, but I am still in love.",
           26:"God gave us the senses to let us feel the love in everyone's heart, not the illusions brought about by wealth.",
           27:"Embrace your passion",
           28:"Simplicity is the ultimate sophistication",
           29:"Remembering that you are going to die is the best way I know to avoid the trap of thinking you have something to lose. You are already naked. There is no reason not to follow your heart.",
           30:"Great things in business are never done by one person. They're done by a team of people.",
           31:"An iPod, a phone, an internet mobile communicator... these are NOT three separate devices! And we are calling it iPhone! Today Apple is going to reinvent the phone. And here it is.",
           32:"Computers themselves, and software yet to be developed, will revolutionize the way we learn.",
           33:"Design is a funny word. Some people think design means how it looks. But of course, if you dig deeper, it's really how it works.",
           34:"Technology is nothing. What's important is that you have a faith in people, that they're basically good and smart, and if you give them tools, they'll do wonderful things with them.",
           35:"It's not a faith in technology. It's faith in people."
          }
    return(jobs[gen] + name)

#function for bill gate's quotes
def bill():
    gen = random.randint(1,50)
    name = " --Bill Gates"
    bill = {
           1:"Success is a lousy teacher. It seduces smart people into thinking they can't lose.",
           2:"The first rule of any technology used in a business is that automation applied to an efficient operation will magnify the efficiency. The second is that automation applied to an inefficient operation will magnify the inefficiency.",
           3:"It's fine to celebrate success but it is more important to heed the lessons of failure.",
           4:"We always overestimate the change that will occur in the next two years and underestimate the change that will occur in the next ten. Don't let yourself be lulled into inaction.",
           5:"Your most unhappy customers are your greatest source of learning. Share this Quote",
           6:"If you can't make it good, at least make it look good. Share this Quote",
           7:"The Internet is becoming the town square for the global village of tomorrow.",
           8:"We all need people who will give us feedback. That's how we improve.",
           9:"If you go back to 1800, everybody was poor. I mean everybody. The Industrial Revolution kicked in, and a lot of countries benefited, but by no means everyone.",
           10:"As we look ahead into the next century, leaders will be those who empower others.",
           11:"The advance of technology is based on making it fit in so that you don't really even notice it, so it's part of everyday life.",
           12:"Information technology and business are becoming inextricably interwoven. I don't think anybody can talk meaningfully about one without the talking about the other.",
           13:"Software is a great combination between artistry and engineering.",
           14:"The intersection of law, politics, and technology is going to force a lot of good thinking. Share this Quote",
           15:"Climate change is a terrible problem, and it absolutely needs to be solved. It deserves to be a huge priority.",
           16:"Technology is just a tool. In terms of getting the kids working together and motivating them, the teacher is the most important.",
           17:"Intellectual property has the shelf life of a banana.",
           18:"When I was growing up, my parents were almost involved in various volunteer things. My dad was head of Planned Parenthood. And it was very controversial to be involved with that.",
           19:"I think it's fair to say that personal computers have become the most empowering tool we've ever created. They're tools of communication, they're tools of creativity, and they can be shaped by their user",
           20:"Discrimination has a lot of layers that make it tough for minorities to get a leg up.",
           21:"Everyone needs a coach. It doesn't matter whether you're a basketball player, a tennis player, a gymnast or a bridge player.",
           22:"I really had a lot of dreams when I was a kid, and I think a great deal of that grew out of the fact that I had a chance to read a lot.",
           23:"Drones overall will be more impactful than I think people recognize, in positive ways to help society. Share this Quote",
           24:"I never took a day off in my twenties. Not one. And I'm still fanatical, but now I'm a little less fanatical. Share this Quote",
           25:"Treatment without prevention is simply unsustainable.",
           26:"You may have heard of Black Friday and Cyber Monday. There's another day you might want to know about: Giving Tuesday. The idea is pretty straightforward. On the Tuesday after Thanksgiving, shoppers take a break from their gift-buying and donate what they can to charity.",
           27:"By improving health, empowering women, population growth comes down. ",
           28:"Microsoft is not about greed. It's about innovation and fairness.",
           29:"Nuclear energy, in terms of an overall safety record, is better than other energy.",
           30:"Historically, privacy was almost implicit, because it was hard to find and gather information. But in the digital world, whether it's digital cameras or satellites or just what you click on, we need to have more explicit rules - not just for governments but for private companies.",
           31:"Security is, I would say, our top priority because for all the exciting things you will be able to do with computers - organizing your lives, staying in touch with people, being creative - if we don't solve these security problems, then people will hold back.",
           32:"I believe in innovation and that the way you get innovation is you fund research and you learn the basic facts.",
           33:"We've got to put a lot of money into changing behavior.",
           34:"I'm a great believer that any tool that enhances communication has profound effects in terms of how people can learn from each other, and how they can achieve the kind of freedoms that they're interested in.",
           35:"Technology is unlocking the innate compassion we have for our fellow human beings.",
           36:"In the long run, your human capital is your main base of competition. Your leading indicator of where you're going to be 20 years from now is how well you're doing in your education system.",
           37:"Legacy is a stupid thing! I don't want a legacy.",
           38:"We make the future sustainable when we invest in the poor, not when we insist on their suffering.",
           39:"The future of advertising is the Internet.",
           40:"In business, the idea of measuring what you are doing, picking the measurements that count like customer satisfaction and performance... you thrive on that.",
           41:"If your culture doesn't like geeks, you are in real trouble.",
           42:"People always fear change. People feared electricity when it was invented, didn't they? People feared coal, they feared gas-powered engines... There will always be ignorance, and ignorance leads to fear. But with time, people will come to accept their silicon masters.",
           43:"I believe that if you show people the problems and you show them the solutions they will be moved to act.",
           44:"If GM had kept up with technology like the computer industry has, we would all be driving $25 cars that got 1,000 MPG. Share this Quote",
           45:"Research shows that there is only half as much variation in student achievement between schools as there is among classrooms in the same school. If you want your child to get the best education possible, it is actually more important to get him assigned to a great teacher than to a great school.",
           46:"I have seen firsthand that agricultural science has enormous potential to increase the yields of small farmers and lift them out of hunger and poverty.",
           47:"Digital technology has several features that can make it much easier for teachers to pay special attention to all their students.",
           48:"Headlines, in a way, are what mislead you because bad news is a headline, and gradual improvement is not.",
           49:"Money has no utility to me beyond a certain point.",
           50:"The best teacher is very interactive."
          }
    return(bill[gen] + name)

#function for Elun Musk quotes
def elun():
    gen = random.randint(1,50)
    name = " --Elun Musk"
    elun = {
           1:"When something is important enough, you do it even if the odds are not in your favor.",
           2:"I'd rather be optimistic and wrong than pessimistic and right. Share this Quote",
           3:"Patience is a virtue, and I'm learning patience. It's a tough lesson. Share this Quote",
           4:"If something's important enough, you should try. Even if - the probable outcome is failure.",
           5:"Life is too short for long-term grudges.",
           6:"Some people don't like change, but you need to embrace change if the alternative is disaster.",
           7:"I think it's very important to have a feedback loop, where you're constantly thinking about what you've done and how you could be doing it better. I think that's the single best piece of advice: constantly think about how you could be doing things better and questioning yourself.",
           8:"I think there should be regulations on social media to the degree that it negatively affects the public good.",
           9:"If you're trying to create a company, it's like baking a cake. You have to have all the ingredients in the right proportion.",
           10:"I would like to die on Mars. Just not on impact.",
           11:"If you get up in the morning and think the future is going to be better, it is a bright day. Otherwise, it's not.",
           12:"It's OK to have your eggs in one basket as long as you control what happens to that basket.",
           13:"I think it matters whether someone has a good heart.",
           14:"People work better when they know what the goal is and why. It is important that people look forward to coming to work in the morning and enjoy working. ",
           15:"We're running the most dangerous experiment in history right now, which is to see how much carbon dioxide the atmosphere... can handle before there is an environmental catastrophe.",
           16:"I think that's the single best piece of advice: constantly think about how you could be doing things better and questioning yourself.",
           17:"Self-driving cars are the natural extension of active safety and obviously something we should do.",
           18:"I always invest my own money in the companies that I create. I don't believe in the whole thing of just using other people's money. I don't think that's right. I'm not going to ask other people to invest in something if I'm not prepared to do so myself.",
           19:"When I was in college, I wanted to be involved in things that would change the world.",
           20:"People should pursue what they're passionate about. That will make them happier than pretty much anything else.",
           21:"It's very important to like the people you work with. Otherwise, your job is going to be quite miserable.",
           22:"We can't have, like, willy-nilly proliferation of fake news. That's crazy. You can't have more types of fake news than real news. That's allowing public deception to go unchecked. That's crazy.",
           23:"I really do encourage other manufacturers to bring electric cars to market. It's a good thing, and they need to bring it to market and keep iterating and improving and make better and better electric cars, and that's what going to result in humanity achieving a sustainable transport future. I wish it was growing faster than it is.",
           24:"If I'm not in love, if I'm not with a long-term companion, I cannot be happy.",
           25:"There have to be reasons that you get up in the morning and you want to live. Why do you want to live? What's the point? What inspires you? What do you love about the future? If the future does not include being out there among the stars and being a multi-planet species, I find that incredibly depressing.",
           26:"The future of humanity is going to bifurcate in two directions: Either it's going to become multiplanetary, or it's going to remain confined to one planet and eventually there's going to be an extinction event.",
           27:"Great companies are built on great products.",
           28:"I think we are at the dawn of a new era in commercial space exploration.",
           29:"Rockets are cool. There's no getting around that.",
           30:"The value of beauty and inspiration is very much underrated, no question. But I want to be clear: I'm not trying to be anyone's savior. I'm just trying to think about the future and not be sad.",
           31:"I think we have a duty to maintain the light of consciousness to make sure it continues into the future.",
           32:"Brand is just a perception, and perception will match reality over time. Sometimes it will be ahead, other times it will be behind. But brand is simply a collective impression some have about a product.",
           33:"A company is a group organized to create a product or service, and it is only as good as its people and how excited they are about creating. I do want to recognize a ton of super-talented people. I just happen to be the face of the companies.",
           34:"If we drive down the cost of transportation in space, we can do great things.",
           35:"There's a silly notion that failure's not an option at NASA. Failure is an option here. If things are not failing, you are not innovating enough.",
           36:"To make an embarrassing admission, I like video games. That's what got me into software engineering when I was a kid. I wanted to make money so I could buy a better computer to play better video games - nothing like saving the world",
           37:"The problem is that at a lot of big companies, process becomes a substitute for thinking. You're encouraged to behave like a little gear in a complex machine. Frankly, it allows you to keep people who aren't that smart, who aren't that creative.",
           38:"If you're entering anything where there's an existing marketplace, against large, entrenched competitors, then your product or service needs to be much better than theirs. It can't be a little bit better, because then you put yourself in the shoes of the consumer... you're always going to buy the trusted brand unless there's a big difference.",
           39:"Any product that needs a manual to work is broken.",
           40:"If humanity doesn't land on Mars in my lifetime, I would be very disappointed.",
           41:"I'm interested in things that change the world or that affect the future and wondrous, new technology where you see it, and you're like, 'Wow, how did that even happen? How is that possible?",
           42:"We're already cyborgs. Your phone and your computer are extensions of you, but the interface is through finger movements or speech, which are very slow.",
           43:"With artificial intelligence, we are summoning the demon. You know all those stories where there's the guy with the pentagram and the holy water, and he's like, yeah, he's sure he can control the demon? Doesn't work out.",
           44:"Tesla is here to stay and keep fighting for the electric car revolution.",
           45:"You could warm Mars up, over time, with greenhouse gases.",
           46:"Starting a business is not for everyone. Starting a business - I'd say, number one is have a high pain threshold.",
           47:"If you don't have sustainable energy, you have unsustainable energy. The fundamental value of a company like Tesla is the degree to which it accelerates the advent of sustainable energy faster than it would otherwise occur.",
           48:"Really, the only thing that makes sense is to strive for greater collective enlightenment.",
           49:"I tend to approach things from a physics framework. And physics teaches you to reason from first principles rather than by analogy.",
           50:"The goal of Tesla is to accelerate sustainable energy, so we're going to take a step back and think about what's most likely to achieve that goal."
          }
    return(elun[gen] + name)

#function for Nickolas Tesla quotes
def tesla():
    gen = random.randint(1,42)
    name = " --Nickolas Tesla"
    tesla = {
           1:"The desire that guides me in all I do is the desire to harness the forces of nature to the service of mankind.",
           2:"Our senses enable us to perceive only a minute portion of the outside world.",
           3:"Life is and will ever remain an equation incapable of solution, but it contains certain known factors.",
           4:"I hope this is the invention that will make war impossible.",
           5:"If your hate could be turned into electricity, it would light up the whole world.",
           6:"What one man calls God, another calls the laws of physics.”",
           7:"It's not the love you make. It's the love you give",
           8:"Great moments are born from great opportunity.",
           9:"A new idea must not be judged by its immediate results.",
           10:"One's salvation could only be brought about through his own efforts.",
           11:"Modern science says: 'The sun is the past, the earth is the present, the moon is the future.' From an incandescent mass we have originated, and into a frozen mass we shall turn. Merciless is the law of nature, and rapidly and irresistibly we are drawn to our doom.",
           12:"Let the future tell the truth, and evaluate each one according to his work and accomplishments. The present is theirs; the future, for which I have really worked, is mine.",
           13:"It is paradoxical, yet true, to say, that the more we know, the more ignorant we become in the absolute sense, for it is only through enlightenment that we become conscious of our limitations. Precisely one of the most gratifying results of intellectual evolution is the continuous opening up of new and greater prospects.",
           14:"Today's scientists have substituted mathematics for experiments, and they wander off through equation after equation, and eventually build a structure which has no relation to reality.",
           15:"The scientists of today think deeply instead of clearly. One must be sane to think clearly, but one can think deeply and be quite insane.",
           16:"I don't care that they stole my idea… I care that they don't have any of their own",
           17:"I do not think you can name many great inventions that have been made by married men.",
           18:"Our virtues and our failings are inseparable, like force and matter. When they separate, man is no more.",
           19:"Every living being is an engine geared to the wheelwork of the universe. Though seemingly affected only by its immediate surrounding, the sphere of external influence extends to infinite distance.",
           20:"The spread of civilisation may be likened to a fire; first, a feeble spark, next a flickering flame, then a mighty blaze, ever increasing in speed and power.",
           21:"In the twenty-first century, the robot will take the place which slave labor occupied in ancient civilization.",
           22:"The human being is a self-propelled automaton entirely under the control of external influences. Willful and predetermined though they appear, his actions are governed not from within, but from without. He is like a float tossed about by the waves of a turbulent sea.",
           23:"The harness of waterfalls is the most economical method known for drawing energy from the sun.",
           24:"The harness of waterfalls is the most economical method known for drawing energy from the sun.",
           25:"If you want to find the secrets of the universe, think in terms of energy, frequency and vibration.",
           26:"We all make mistakes, and it is better to make them before we begin.",
           27:"Be alone, that is the secret of invention; be alone, that is when ideas are born.",
           28:"A new idea must not be judged by its immediate results.",
           29:"If your hate could be turned into electricity, it would light up the whole world.",
           30:"Of all the frictional resistances, the one that most retards human movement is ignorance.",
           31:"Our entire biological system, the brain, and the Earth itself, work on the same frequencies.",
           32:"If you only knew the magnificence of the 3, 6 and 9, then you would have the key to the universe.",
           33:"Peace can only come as a natural consequence of universal enlightenment.",
           34:"The gift of mental power comes from God, Divine Being, and if we concentrate our minds on that truth, we become in tune with this great power. My Mother had taught me to seek all truth in the Bible.",
           35:"To know each other we must reach beyond the sphere of our sense perceptions.",
           36:"The desire that guides me in all I do is the desire to harness the forces of nature to the service of mankind.",
           37:"Originality thrives in seclusion free of outside influences",
           38:"Though free to think and act, we are held together, like the stars in the firmament, with ties inseparable. These ties cannot be seen, but we can feel them.",
           39:"The day science begins to study non-physical phenomena, it will make more progress in one decade than in all the previous centuries of its existence.",
           40:"But instinct is something which transcends knowledge. We have, undoubtedly, certain finer fibers that enable us to perceive truths when logical deduction, or any other willful effort of the brain, is futile.",
           41:"The opinion of the world does not affect me. I have placed as the real values in my life what follows when I am dead.",
           42:"My wireless transmitter does not use Hertzian waves, which are a grievous myth, but sound waves in the aether."
   
          }
    return(tesla[gen] + name)

#function for Albert Einstein quotes
def einstein():
    gen = random.randint(1,30)
    name = " --Albert Einstein"
    einstein = {
           1:"We are slowed down sound and light waves, a walking bundle of frequencies tuned into the cosmos. We are souls dressed up in sacred biochemical garments and our bodies are the instruments through which our souls play their music.",
           2:"Weak people revenge. Strong people forgive. Intelligent People Ignore.",
           3:"The difference between stupidity and genius is that genius has its limits.",
           4:"We can't solve today's problems with the mentality that created them.",
           5:"Everybody is a genius. But if you judge a fish by its ability to climb a tree, it will live its whole life believing that it is stupid.",
           6:"The world will not be destroyed by those who do evil, but by those who watch them without doing anything.",
           7:"The only thing more dangerous than ignorance is arrogance",
           8:"Information is not knowledge. The only source of knowledge is experience. You need experience to gain wisdom.",
           9:"Failure is success in progress",
           10:"Don't listen to the person who has the answers; listen to the person who has the questions.",
           11:"Insanity: doing the same thing over and over again and expecting different results.",
           12:"Everything that exists in your life, does so because of two things: something you did or something you didn't do.",
           13:"Cherish the questions, for the answers keep changing.",
           14:"The more I study science, the more I believe in God.",
           15:"Thinking is hard work; that's why so few do it.",
           16:"The leader is one who, out of the clutter, brings simplicity... out of discord, harmony... and out of difficulty, opportunity.",
           17:"Life is like riding a bicycle. To keep your balance, you must keep moving.",
           18:"artificial intellegance is no match for natural stupidity",
           19:"A ship is always safe at the shore - but that is NOT what it is built for.",
           20:"Knowledge and ego are directly related. the less knowledge, the greater the ego",
           21:"Be a voice not an echo.",
           22:"Everyone knew it was impossible, until a fool who didn't know came along and did it.",
           23:"God did not create evil. Just as darkness is the absence of light, evil is the absence of God.",
           24:"Don't wait for miracles, your whole life is a miracle.",
           25:"We cannot solve our problems with the same thinking we used when we created them.",
           26:"Learn from yesterday, live for today, hope for tomorrow. The important thing is not to stop questioning.",
           27:"We cannot solve our problems with the same thinking we used when we created them.",
           28:"A person who never made a mistake never tried anything new.",
           29:"Look deep into nature, and then you will understand everything better.",
           30:"The world is a dangerous place to live; not because of the people who are evil, but because of the people who don't do anything about it.",
          }
    return(einstein[gen] + name)

#function for scientist quotes
def science():
    gen = random.randint(1,50)
    name = " --Scientist"
    science = {
           1:"There must be no barriers to freedom of inquiry. There is no place for dogma in science. The scientist is free, and must be free to ask any question, to doubt any assertion, to seek for any evidence, to correct any errors.",
           2:"Most people say that it is the intellect which makes a great scientist. They are wrong: it is character.",
           3:"A scientist in his laboratory is not a mere technician: he is also a child confronting natural phenomena that impress him as though they were fairy tales.",
           4:"If an elderly but distinguished scientist says that something is possible, he is almost certainly right; but if he says that it is impossible, he is very probably wrong.",
           5:"It is a good morning exercise for a research scientist to discard a pet hypothesis every day before breakfast. It keeps him young.",
           6:"A good scientist is a person with original ideas. A good engineer is a person who makes a design that works with as few original ideas as possible. There are no prima donnas in engineering.",
           7:"The scientist is motivated primarily by curiosity and a desire for truth.",
           8:"I believe that a scientist looking at nonscientific problems is just as dumb as the next guy.",
           9:"The scientist is not a person who gives the right answers, he is one who asks the right questions.",
           10:"I may be a Jewish scientist, but I would be tickled silly if one day I were reincarnated as a Baptist preacher.",
           11:"The best scientist is open to experience and begins with romance - the idea that anything is possible",
           12:"If you're a social scientist worth your salt, you never do a univariate analysis.",
           13:"I was married to Margaret Joan Howe in 1940. Although not a scientist herself she has contributed more to my work than anyone else by providing a peaceful and happy home.",
           14:"The combined results of several people working together is often much more effective than could be that of an individual scientist working alone.",
           15:"Everybody's a mad scientist, and life is their lab. We're all trying to experiment to find a way to live, to solve problems, to fend off madness and chaos.",
           16:"A starry sky is equally interesting to a scientist, a mystic, an ethics scholar, and a poet. Looking at the stars, each experiences something different, and each sees his own picture.",
           17:"I felt that chess... is a science in the form of a game... I consider myself a scientist. I wanted to be treated like a scientist.",
           18:"I'm not a gentleman and I'm not a scientist.",
           19:"What is a scientist after all? It is a curious man looking through a keyhole, the keyhole of nature, trying to know what's going on.",
           20:"A writer should have the precision of a poet and the imagination of a scientist.",
           21:"I always felt that a scientist owes the world only one thing, and that is the truth as he sees it.",
           22:"But I don't see myself as a woman in science. I see myself as a scientist.",
           23:"The scientist only imposes two things, namely truth and sincerity, imposes them upon himself and upon other scientists.",
           24:"The greatest enemy of knowledge is not ignorance, it is the illusion of knowledge.",
           25:"In science, there are no shortcuts to truth.",
           26:"Science is not only a disciple of reason but also one of romance and passion.",
           27:"The more I learn, the more I realize how much I don't know.",
           28:"The best way to predict the future is to create it.",
           29:"The only source of knowledge is experience.",
           30:"The greatest glory in living lies not in never falling, but in rising every time we fall.",
           31:"Science knows no country, because knowledge belongs to humanity, and is the torch which illuminates the world.",
           32:"The universe is under no obligation to make sense to you.",
           33:"Science is a way of thinking much more than it is a body of knowledge.",
           34:"The greatest discoveries often lie not in finding new things, but in seeing familiar things in new ways.",
           35:"The only true wisdom is in knowing you know nothing.",
           36:"The pursuit of science is a never-ending journey into the unknown, fueled by curiosity and guided by reason",
           37:"The only thing standing between you and your goal is the story you keep telling yourself as to why you can't achieve it.",
           38:"The scientific method is nothing but the expression of the necessity of the elementary rules of formal logic.",
           39:"The best scientists are open to the possibility that they may be wrong, and they are willing to change their minds in the face of new evidence.",
           40:"The greatest triumphs of science are born out of the struggles and failures of countless experiments.",
           41:"Science is the poetry of reality.",
           42:"The most beautiful experience we can have is the mysterious.",
           43:"Science is the key to unlocking the mysteries of the universe and harnessing its power for the benefit of humanity.",
           44:"Imagination is more important than knowledge.",
           45:"The only limit to our realization of tomorrow will be our doubts of today.",
           46:"Science is a way of thinking, not just a body of knowledge.",
           47:"It is not the strongest of the species that survives, nor the most intelligent. It is the one most responsive to change.",
           48:"The true sign of intelligence is not knowledge, but imagination.",
           49:"The greatest scientists are also the greatest dreamers, constantly envisioning new possibilities and exploring uncharted territories of the mind.",
           50:"Science is not about being right or wrong, it's about being willing to ask the right questions and follow the evidence wherever it leads"
          }
    return(science[gen] + name)

#function for hackers quotes
def hackers():
    gen = random.randint(1,50)
    name = " --Hackers"
    hackers = {
           1:"I'm a hacker, but I'm the good kind of hackers. And I've never been a criminal.",
           2:"Social engineering has become about 75 percent of an average hacker's toolkit, and for the most successful hackers, it reaches 90 percent or more.",
           3:"When hackers have access to powerful computers that use brute force hacking, they can crack almost any password; even one user with insecure access being successfully hacked can result in a major breach.",
           4:"The workstation-class machines built by Sun and others opened up new worlds for hackers.",
           5:"No night of drinking or drugs or sex could ever compare to a long evening of productive hacking.",
           6:"The internet is the most important tool for disseminating information we've had since the invention of the printing press. Unfortunately, it's also one of the best ways of stealing or suppressing information and for putting out misinformation.",
           7:"Don't Hate me, Hate that Code",
           8:"The only way to maintain privacy on the internet is to not be on the internet.",
           9:"To hack a system requires getting to know its rules better than the people who created it or are running it, and exploiting all the vulnerable distance between how those people had intended the system to work and how it actually works, or could be made to work.",
           10:"Beware of geeks bearing gifts",
           11:"Internet and privacy are antithesis of each other.",
           12:"There Could be something more Dangerous Behind that Firewall",
           13:"It is common knowledge in the programmer's circle that almost every smartphone in the world is infected with some form of trojan.",
           14:"Anything that says 'smart' in front of its name, is a potential magnet for trojans. The same goes for anything that is endorsed as 'open source'.",
           15:"Darkness envelopes technology where only a select few gain access to the light switch.",
           16:"When solving problems, dig at the roots instead of just hacking at the leaves.",
           17:"As a young boy, I was taught in high school that hacking was cool.",
           18:"Is hacking ever acceptable? It depends on the motive.",
           19:"There are a thousand hacking at the branches of evil to one who is striking at the root.",
           20:"When hackers have access to powerful computers that use brute force hacking, they can crack almost any password; even one user with insecure access being successfully hacked can result in a major breach.",
           21:"My primary goal of hacking was the intellectual curiosity, the seduction of adventure.",
           22:"A lot of hacking is playing with other people, you know, getting them to do strange things.",
           23:"What was once a comparatively minor threat - people hacking for fun or for bragging rights - has turned into full-blown economic espionage and extremely lucrative cyber crime.",
           24:"I was addicted to hacking, more for the intellectual challenge, the curiosity, the seduction of adventure; not for stealing, or causing damage or writing computer viruses.",
           25:"Growth hacking is a mindset, and those who have it will reap incredible gains. Share this Quote",
           26:"Hackers are breaking the systems for profit. Before, it was about intellectual curiosity and pursuit of knowledge and thrill, and now hacking is big business.",
           27:"There is the possibility to be suddenly arrested for hacking.",
           28:"It is a fairly open secret that almost all systems can be hacked, somehow. It is a less spoken of secret that such hacking has actually gone quite mainstream.",
           29:"Eitan Hersh wrote a book in 2015 called 'Hacking the Electorate.' It's pretty much the best book I've seen on the use of data science in U.S. elections and what good evidence shows works and does not work.",
           30:"Hacking is exploiting security controls either in a technical, physical or a human-based element.",
           31:"The hacking trend has definitely turned criminal because of e-commerce.",
           32:"Problem-solving, inventing, hacking and coding is more of an adrenaline rush of endorphins rather than a feeling.",
           33:"I was hooked in before hacking was even illegal.",
           34:"I'm interested to see what happens with Fox News and phone hacking. I really can't believe it just happens in Great Britain. Because really, who cares about just hacking phones over there?",
           35:"The idea of having no responsibilities except general edification seems like such a luxury now. When I had it, all I wanted to do was hack around on the Web. Now the vast majority of my hours are hacking around on the Web.",
           36:"That was the division in the hacking world: There were people who were exploring it and the people who were trying to make money from it. And, generally, you stayed away from anyone who was trying to make money from it.",
           37:"My hacking involved pretty much exploring computer systems and obtaining access to the source code of telecommunication systems and computer operating systems, because my goal was to learn all I can about security vulnerabilities within these systems.",
           38:"Further, the next generation of terrorists will grow up in a digital world, with ever more powerful and easy-to-use hacking tools at their disposal.",
           39:"Computer hacking really results in financial losses and hassles. The objectives of terrorist groups are more serious. That is not to say that cyber groups can't access a telephone switch in Manhattan on a day like 9/11, shut it down, and therefore cause more casualties.",
           40:"Flying down a tunnel of 1s and 0s is not how hacking is really done.",
           41:"Hacking into a victim of crime's phone is a sort of poetically elegant manifestation of a modus operandi the tabloids have.",
           42:"Growth hacking is the future of marketing. It has to be.",
           43:"One of my favourite books about hackers is 'Masters of Deception' about this hacking group in the 1990s. Many of them didn't come from wealthy families. These are kids that are very intelligent; they just happen to be misdirected.",
           44:"Everybody has a hacking capability. And probably every intelligence service is hacking in the territory of other countries. But who exactly does what? That would be a very sensitive piece of information. But it's very difficult to communicate about it. Because nobody wants to admit the scope of what they're doing.",
           45:"Really, what the government is asking Apple to do is to make every individual who uses an iPhone susceptible to hacking by bad people, foreign governments, and anyone who wants.",
           46:"I could have evaded the FBI a lot longer if I had been able to control my passion for hacking.",
           47:"I started with CB radio, ham radio, and eventually went into computers. And I was just fascinated with it. And back then, when I was in school, computer hacking was encouraged. It was an encouraged activity. In fact, I remember one of the projects my teacher gave me was writing a log-in simulator.",
           48:"My actions constituted pure hacking that resulted in relatively trivial expenses for the companies involved, despite the government's false claims.",
           49:"My actions constituted pure hacking that resulted in relatively trivial expenses for the companies involved, despite the government's false claims.",
           50:"It was a hobby I got into a long time ago, hacking cameras. I was able to make my own using different lenses."
          }
    return(hackers[gen] + name)

#function for success quotes
def success():
    gen = random.randint(1,50)
    name = " --leaders"
    success = {
           1:"Perseverance goes a long way",
           2:"Don't let your circumstances hold you back",
           3:"Obstacles are inevitable, but quitting isn't",
           4:"You don't need to wait for permission to succeed",
           5:"Sometimes, success means being the first to fail",
           6:"It's all about daily, consistent action",
           7:"Sometimes, you have to make sacrifices to succeed",
           8:"Isn't it funny how that works?",
           9:"Your mindset is everything",
           10:"Only listen to those who are already where you want to be",
           11:"There's no deadline for success",
           12:"You've got to give it your all",
           13:"They're not always the same thing",
           14:"Because it was easy, everyone would do it",
           15:"It's rarely a smooth journey",
           16:"It's the perfect formula",
           17:"Tune out the naysayers",
           18:"Don't let it keep you down for long",
           19:"A great reminder to not get too caught up in the pursuit of success",
           20:"The perfect time to begin is now",
           21:"It's all about the learning process",
           22:"You've got to put in the hard yards",
           23:"Because it always seems impossible until it's done",
           24:"Resilience is the key",
           25:"Look for evidence why you can do it, not for why you shouldn't",
           26:"A simple yet effective mantra for success",
           27:"There is a powerful driving force inside every human being that, once unleashed, can make any vision, dream, or desire a reality.",
           28:"The successful warrior is the average man, with laser-like focus.",
           29:"Extraordinary results call for extraordinary effort",
           30:"Do today what others won't and achieve tomorrow what others can't.",
           31:"The distance between insanity and genius is measured only by success.",
           32:"I never dreamed about success, I worked for it — Estee Lauder.",
           33:"There's no substitute for taking action",
           34:"I attribute my success to this: I never gave or took any excuse.",
           35:"Don't let the fear of losing be greater than the excitement of winning— Robert Kiyosaki.",
           36:"The secret of success is to do the common thing uncommonly well.",
           37:"It's okay not to have it all figured out",
           38:"You don't have to see the whole staircase, just take the first step.",
           39:"You don't have to see the whole staircase, just take the first step The difference between a successful person and others is not a lack of knowledge, but a lack of will..",
           40:"Willpower will get you everywhere, The difference between a successful person and others is not a lack of knowledge, but a lack of will.",
           41:"It's not always easy, but it's worth it, There's no elevator to success. You have to take the stairs.",
           42:"You just have to keep going, Success is not the absence of failure, it's persistence through failure.",
           43:"Success is the good fortune that comes from aspiration, desperation, perspiration and inspiration.",
           44:"Sometimes in order to get, you need to first give — Napoleon Hill",
           45:"Don't underestimate its power, For success, attitude is equally as important as ability.",
           46:"What you don't know can be just as valuable as what you do",
           47:"Things may come to those who wait, but only the things left by those who hustle.",
           48:"Don't be afraid to try and fail",
           49:"The master has failed more times than the beginner has even tried.",
           50:"Getting started is the most important part"
          }
    return(success[gen] + name)
def all():
    gen = random.randint(1,9)
    job = jobs()
    zuck = mark()
    gates = bill()
    musk = elun()
    nick = tesla()
    albert = einstein()
    sci = science()
    hack = hackers()
    suc = success()
    
    if gen == 1:
        return job
    
    elif gen == 2:
        return zuck
    
    elif gen == 3:
        return gates
    
    elif gen == 4:
        return musk
    
    elif gen == 5:
        return nick
    
    elif gen == 6:
        return albert
    
    elif gen == 7:
        return sci
    
    elif gen == 8:
        return hack

    elif gen == 9:
        return suc
    
    else:
        return " error occured check package"
