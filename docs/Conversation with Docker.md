# My conversation with Docker.
**My first mail :**


Hello,

  

I would like to take this opportunity to thank you for the great tool you have created.

  

I am a cyber security researcher, and recently I have stumbled upon an potential side-channel vulnerability I believe should be reported to you.

  

I would like to address this vulnerability and present you with an exploit POC I created.

  

By exploiting this vulnerability, it is possible for containers to communicate with each other, even when the two should not have any network communication with each other.

  

As I am sure you are aware of, and it has been brought up before, every container has access to information regarding the ram usage of the host.

  

In addition, a container can change the ram usage of the host by a few simple procedures, such as allocating memory using a simple python script.

  

I have created a simple POC that implements a basic C&C infrastructure using a python command server that simply allocates a large amount of memory (e.g. 200MB) in constant intervals. In each interval, the program either allocates a memory chunk or doesn’t do so, in order to signal “1” or “0” respectively.

The other container just translates these binary signals to commands and runs them using a simple encoding protocol.

  

I have attached the POC. Keep in mind it is a very naive implementation and could be further refined in order to achieve faster transfer speeds and higher reliability.

---

**They first answer :**
Thanks for this report (and neat PoC), unfortunately we don't agree that  
this is a vulnerability -- for a few reasons.  
  
1. In order to exploit this you already have two containers that you  
wish to communicate on a target system -- which means that you  
already have code-execution within containers on the system and they  
are mutually co-operative. In other words, there is no "victim"  
process. I'm sure this would be a neat trick if you manage to get  
"blind container execution" to exfiltrate information between  
containers, but given that all the processes are co-operative I don't  
see this as an issue.  
  
2. This issue is actually a kernel issue (/proc/meminfo and the other  
memory-info APIs aren't cgroup-aware, leading to information about  
global system resources being scoped inside the container). As you  
said, this issue has been known about for a really long time -- but  
kernel developers have categorically stated they aren't interested in  
/proc/meminfo becoming cgroup-aware because of how complicated the  
infrastructure would be to make it work. So, we don't really have the  
ability to fix the fundamental issue.  
  
There is a project called LXCFS[1] which allows you to mask  
/proc/meminfo in containers, and you could use this to prevent some  
of the problem -- but there are other memory-info APIs that can't be  
fixed so easily. You could trick them with the new seccomp  
RET_USER_NOTIF API, but that would not help older kernels and so on  
(and ptrace would kill performance in containers by a fair amount,  
and break gdb).  
  
3. Isolating machines to avoid side-channels like this is almost an  
intractable problem -- because at the end of the day you are running  
on the same hardware and there will always be hardware tells (latency  
in HDD access or even CPU load -- both can be limited with cgroups  
but you'd likely be able to tell). Even VMs are vulnerable to  
side-channels like this, because shared-tenant systems fundamentally  
have to share resources that aren't designed to be side-channel  
resistant.  
  
We do appreciate you reporting this, and hope you'll continue to  
disclose potential issues to us in the future. :D  
  
[1]: [https://linuxcontainers.org/lxcfs/introduction/](https://linuxcontainers.org/lxcfs/introduction/)

---
**My second mail:**
Hey, thank you for the quick response.

  

Although I agree with most of your response, there are a few comments you have made I have a hard time agreeing with.

  

Regarding what you wrote in paragraph 1, it is true that an adversary needs code execution on both containers but it's important to understand that people who use Docker rely on the fact that there is a network isolation between containers in different namespaces. For example if someone configures his two containers with “--network=none” for them to run as “standalone” or even just to isolate them from each other on the network perspective. What I showed with my POC is that there is a way for them to communicate. This is why I have a hard time with accepting your answer about it not being a issue.

I have uploaded a short video showcasing the POC which I sent you previously.

  

[https://youtu.be/dOuzpxdQyUw](https://youtu.be/dOuzpxdQyUw)

  

Moreover, I found in your documentation regarding namespaces:

“Namespaces provide the first and most straightforward form of isolation: processes running within a container cannot see, and even less affect, processes running in another container, or in the host system.”

--  [https://docs.docker.com/engine/security/security/](https://docs.docker.com/engine/security/security/)

  

People rely on this definition!

  

In regards to paragraph 2, I can only agree. The scope of this problem is greater and resids with linux kernel developers and I think they should at least be aware of it.

  

Thank you for the info about LXCFS, I will look into it.

  

In regards to paragraph 3, in some sense I agree that side-channel attacks are always an issue when using virtualization as an isolation. But, in this case I found it to be much easier.

  

FYI, i’m writing an article about it for public knowledge.

  

Thank you

---

**My third mail:** (second and third was sent one after one in the same day...)
Hi, I want to share with you a new thing that I found.

  

I have been reading this great article

  

[https://fabiokung.com/2014/03/13/memory-inside-linux-containers/](https://fabiokung.com/2014/03/13/memory-inside-linux-containers/)

  

And found this interesting paragraph:

  

“/proc is not the only issue:

sysinfo

  

Even if we could find a solution to containerize /proc/meminfo with which everyone is happy, it would not be enough.

  

Linux also provides the sysinfo(2) syscall, which returns information about system resources (e.g. memory). As with /proc/meminfo, it is not containerized: it always returns metrics for the box as a whole”

  

So i read about sysinfo and saw this:

  

Since Linux 2.3.23 (i386) and Linux 2.3.48 (all architectures) the

structure is:

  

struct sysinfo {

long uptime; /* Seconds since boot */

unsigned long loads[3]; /* 1, 5, and 15 minute load averages */

unsigned long totalram; /* Total usable main memory size */

unsigned long freeram; /* Available memory size */

unsigned long sharedram; /* Amount of shared memory */

unsigned long bufferram; /* Memory used by buffers */

unsigned long totalswap; /* Total swap space size */

unsigned long freeswap; /* Swap space still available */

unsigned short procs; /* Number of current processes */

unsigned long totalhigh; /* Total high memory size */

unsigned long freehigh; /* Available high memory size */

unsigned int mem_unit; /* Memory unit size in bytes */

char _f[20-2*sizeof(long)-sizeof(int)];

 /* Padding to 64 bytes */

};

  

There is a field called procs that holds the number of processes running inside the host.

  

So I checked it up in my own docker environment

And I noticed that I can create processes in one container and see the amount of processes in the other container

  

I'm positively sure that if we would have delved into it a little more we could find more flaws that can be used in a side channel attack scenario

  

I haven't created a new POC that uses “procs” like I created in meminfo, but I definitely can.

  

The reason that I am sharing this issue with you is so that other people that use Docker should be aware that Docker does not offer the same isolation that VM’s have. (on a side note, I do enjoy using docker and think it's a great tool)

  

Regards,

Yehuda Corsia

---

**They response :**

On 2019-03-18, Yehuda Corsia <[yehudacorsia@gmail.com](mailto:yehudacorsia@gmail.com)> wrote:  
> Even if we could find a solution to containerize /proc/meminfo with which  
> everyone is happy, it would not be enough.  
>  
> Linux also provides the sysinfo(2) syscall, which returns information about  
> system resources (e.g. memory). As with /proc/meminfo, it is not  
> containerized: it always returns metrics for the box as a whole”  
  
Yes, I believe I referenced sysinfo(2) (or at least I was thinking of  
it) when I said that lxcfs is also not a perfect solution. There are  
ways to fake sysinfo(2) too -- since Linux 5.0 there's a seccomp syscall  
emulation framework that is likely going to be used by LXC to further  
fake such information.  
  
The fix to make sysinfo->procs return the number of processes in the  
current PID namespace would be fairly trivial (it was probably  
overlooked) but doing the same thing for memory has the same cgroup  
architecture issues I mentioned in my last email. Obviously I'd be happy  
if this issue was fixed by kernel upstream, but I don't think there's  
much we can do about it.  
  
> I'm positively sure that if we would have delved into it a little more we  
> could find more flaws that can be used in a side channel attack scenario  
>  
> I haven't created a new POC that uses “procs” like I created in meminfo,  
> but I definitely can.  
  
> The reason that I am sharing this issue with you is so that other people  
> that use Docker should be aware that Docker does not offer the same  
> isolation that VM’s have. (on a side note, I do enjoy using docker and  
> think it's a great tool)  
  
I want to point out that "number of pids on the host" isn't really a big  
isolation issue. By the same logic the modules loaded in the kernel is  
also an isolation issue (which you can also read), or backlight screen  
brightness.  
  
Shared-tenant isolation is a very hard (and I would even argue unsolved)  
problem in computing, and I think that side-channels are unfortunately  
going to always be a problem -- for both containers and VMs.  
  
I imagine you also could side-channel by CPU temperature, disk latency,  
or loadavg. And in order to solve those, you would be better off just  
using different physical machines.

On 2019-03-17, Yehuda Corsia <[yehudacorsia@gmail.com](mailto:yehudacorsia@gmail.com)> wrote:  
> Regarding what you wrote in paragraph 1, it is true that an adversary needs  
> code execution on both containers but it's important to understand that  
> people who use Docker rely on the fact that there is a network isolation  
> between containers in different namespaces. For example if someone  
> configures his two containers with “--network=none” for them to run as  
> “standalone” or even just to isolate them from each other on the network  
> perspective.  
  
But they *are* isolated from a network perspective.  
  
> What I showed with my POC is that there is a way for them to  
> communicate. This is why I have a hard time with accepting your answer  
> about it not being a issue.  
  
I didn't say it wasn't an issue, just that it wasn't a vulnerability. I  
would be very happy if this wasn't the case, but I don't agree that this  
is an issue which deserves the label of "vulnerability".  
  
> Moreover, I found in your documentation regarding namespaces:  
> “Namespaces provide the first and most straightforward form of isolation:  
> processes running within a container cannot see, and even less affect,  
> processes running in another container, or in the host system.”  
> --  [https://docs.docker.com/engine/security/security/](https://docs.docker.com/engine/security/security/)  
>  
> People rely on this definition!  
  
You're sending a mail to the OCI security list, not the Docker one. I  
don't work for Docker. :P  
  
I think that definition is okay for a brand-new user, because I would  
argue "cannot see, and even less affect" doesn't include side-channels  
-- because side-channels are simply a side-effect of running multiple  
users' workloads on the same operating system.  
  
As I mentioned, even VMs have side-channel attacks -- I have my doubts  
that this is a problem that would ever be conclusively solved because of  
how difficult it is to avoid side-channels without horrifically ruining  
performance.  
  
The only example of shared multi-tenancy without any side-channels that  
I know of is System-Z LPARs, and those have their own pages of caveats  
before you could argue they are truly isolated partitions.  
  
> In regards to paragraph 3, in some sense I agree that side-channel attacks  
> are always an issue when using virtualization as an isolation. But, in this  
> case I found it to be much easier.  
  
It is fair to say this is much easier than looking at CPU load or other  
such techniques, but given that the information gathered is only useful  
for communicating between two collaborating container processes, it's  
quite limited in its effectiveness.  
  
In particular, it's unclear to me what would be the benefit of  
communicating this way -- if the attacker has the ability to start these  
processes in the first place they could seed them with the information  
they wanted. I'm sure we could come up with a convoluted example where  
this communication would be useful (a cloud host that gives access to  
different pieces of information to different containers, and you could  
use this to collate the information) -- but I think that is a bit of a  
stretch. I would argue the CVSS score for this issue would be 0, because  
there is no impact on integrity, availability, nor confidentiality --  
because only attacker processes are affected by it.  
  
> FYI, i’m writing an article about it for public knowledge.  
  
Sure, I don't mind -- though I would ask you to mention why we don't  
consider it to be a vulnerability (if you're planning on including a  
disclosure timeline).


---

I am still not response to this mail
when that i will response I will share this here :-)