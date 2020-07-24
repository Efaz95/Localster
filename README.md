### Localster

 - [What is it about?](#what-is-it-about)
 - [How it works?](#how-it-works)
 - [Demo for real-time messaging tool](#real-time-messaging-demo)
 - [Future Implementations](#future-implementations)


## What is it about

Localster is an app built to connect local businesses with local influencers.

The idea of this app came from a Facebook post where I was asked to share a small business in my community.
![FB share](https://i.imgur.com/319Klgn.jpg)

Big companies only hire influencers with a large number of following. As a result, local small influencers have hard time finding sponsors. However, our platform connects these influencers with the other businesses who are not looking for big named influencers, instead they are looking for local people to help spread the business within their community. 


## How it works

Businesses like local restaurants can sign up to Localsters and find influencers in their community. They can chat within our platform and if they find each other to be a good fit, the restaurant can then hire the influencer.  Influencers can customize their profile with their Bio and social media links.  

## Real-time Messaging Demo
I have implemented real-time messaging tool using Python and Ajax for the users to communicate.


![messaging demo](http://g.recordit.co/golIhyzPrF.gif)


Controller:
```
@login_required(login_url='login')
def user_messages(request):
    time_now = datetime.datetime.now()
    user = request.user

    if request.method == "POST":
        if 'read' in request.POST:
            un = request.POST.get('read')
            Messages.objects.filter(id=un).update(is_read=True)
        else:
            sender = request.user
            receiver_name = request.POST.get('msg_receiver')
            receiver = User.objects.get(username=receiver_name)
            msg_content = request.POST.get('msg_content')

            Messages.objects.create(sender=sender, receiver=receiver, msg_content=msg_content)

    inbox = Messages.objects.filter(receiver=user).order_by('-timestamp')
    outbox = Messages.objects.filter(sender=user).order_by('-timestamp')

    context = {'inbox': inbox, 'outbox': outbox, 'time_now': time_now}

    return render(request, 'accounts/messages.html', context)
```
Model:
```
class Messages(models.Model):
    sender = models.ForeignKey(User, related_name="sender", on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name="receiver", on_delete=models.CASCADE)
    msg_content = models.TextField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
```

## Searching and Hire Demo

![messaging demo](http://g.recordit.co/OXVDaK6czm.gif)


## In Progress
 - Notification alerts for a new message


## Future Implementations

 - Integrate Payment system to allow businesses pay directly through our platform
 - Improve Messaging tool using Web Sockets 
