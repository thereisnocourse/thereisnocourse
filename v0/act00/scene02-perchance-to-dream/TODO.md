* [ ] Add "Testing compositors : A, B, C, D, E"?
* [ ] Add mini-game puzzle.

help():

```
WS-DOS could not be started due to multiple errors. 

If you really know what you are doing, you can attempt to manually start the operating system. The following functions are available: 

Type "cast()" to send callbacks to actors.

Type "mount()" to deploy actors to the staging area.

Type "stage()" to acquire props and reset the staging area.

Type "perform()" to issue cues and start the main thread.

Type "direct()" to reset the blocking.
```

Functions will error, based on current state:

* Error, stage is not set. -- stage()
* Error, actors not found. -- cast()
* Error, actors are offstage. -- mount()
* Error, actors are frozen. -- direct()
* perform()

