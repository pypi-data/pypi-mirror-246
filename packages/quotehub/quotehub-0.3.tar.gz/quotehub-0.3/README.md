#quotehub is a python package that provides you with random quotes
#how to use:

    import quotehub

    quotes = quotehub.all()
    print(quotes)

#the above instance gives you access to all the quotes
#you can specifie a particular persons quote like bill gates or mark zuckerberg.

    import quotehub

    quotes = quotehub.mark() #for mark zuckerbergs quotes
    print(quotes)

#or
    from quotehub import mark, bill, elun, hackers #etc

    quotes = bill()
    print(quotes)

#list of all the methods you can use are
    quotehub.all()
    quotehub.mark()
    quotehub.jobs()
    quotehub.bill()
    quotehub.elun()
    quotehub.tesla()
    quotehub.einstein()
    quotehub.science()
    quotehub.hackers()
    quotehub.success()

#never the less just print
    import quotehub

    print(dir(quotehub)) to get all the method you can use

#the only dependency this package need is the random module, but you don't need to install it in your program it comes pre-installed.

#please note that this project is open source and open for collaboration, lets grow this quote project.

#visit our github repo fork the repo, git clone on your local pc and send a pull request to us, we 
#will review it and add it to the package
#and don't forget to add a readme file or our doc

#github repo https://github.com/cyber-maphian/quote-hub.git