# observeAliveConnection

![](./observe_con.gif)

Showing network connection, and logging disconnection.

## Usage(Polybar)

First, clone this repository. For example, type shell to

```bash:shell
mkdir ~/.polybar-script/
git clone git@github.com:Kaniyama-t/observeAliveConnection.git
```

Second, open `~/.config/polybar/config` and add module profile at the end

```config:~/.config/polybar/config
[module/observe_connection]
type = custom/script
exec = ~/.polybar-script/observeAliveConnection/concnt.py
tail = true
interval = 1.0
label-padding = 2
```

Third, add `observe_connection` to `modules-right` or `modules-left` parameter.

```config:~/.config/polybar/config(Example)
modules-right = wlan observe_connection pulseaudio battery time
```

If you want to use Monospaced Font, please put the font to `font-6` at polybar's config or modify constant `I3BAR_FONT_MONO` at `concnt.py`.

And finally, press Super+Shift+R to reload i3bar.

## Optional: Scrolling Text

![](./observe_con-scroll.gif)

Modify the code at `line 63` in `concnt.py`

```
-            self.printForI3Bar(msg)
 +           self.printForI3Bar(self.scrollingText(msg))
```

## Optional: Show Recently Long Disconnection

![](./observe_con-recently.gif)

Modify the code at `line 63` in `concnt.py`

```
-            self.printForI3Bar(msg)
 +           self.printForI3Bar(self.recentTimeText(msg))
```

## FAQ

### Where is log's path?

log will generate in `./log` directory as file named `YYYY-MM-DD.log`. For example `2021-06-01.log`.