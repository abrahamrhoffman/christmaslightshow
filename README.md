# christmaslightshow
Code for the Raspberry Pi 4 - 2022 Dexter Co-op Pre-school Christmas Light Show

### Timing vs Duration
The first number in the sequence file is the timing. Timing is when the effect should take place. The duration is the second number. This informs `lightshow` how long the action should take to complete. If the duration is left blank, the default duration of $1/6$ (for a total of one second if applied to all light channels) is enacted for the action.

For a demonstration of the sequence timings and durations, try `demo.seq` in the sequences folder.

### Sequences
This 2022 lightshow was architected for a float with six poles: three poles on the left and right side.

I named each zone from zero to five. From there, I grouped the channels, representing each side of the float: 0-2 (Group One), 3-5 (Group Two).

To find all the combinations with repetition, you can use itertools' great `product` method:

```
for i in itertools.product([0, 1, 2], [3, 4, 5]):
    print(i)
```

This provides a reasonable starting place for all cross-channel (Group One <-> Group Two) mappings. Next, create some all-channel mappings for variety and "whole-float" effects. Each of these patterns can be used in the `.seq` file in the `sequences` folder. The `lightshow.py` driver application calls an if/then loop, that catches the pattern and triggeres the appropriate GPIOs HIGH or LOW on the Raspberry Pi.

Channel and group mappings used:
```
0 - ZERO
1 - ONE
2 - TWO
3 - THREE
4 - FOUR
5 - FIVE

0,3 - PAIR_ONE
1,4 - PAIR_TWO
2,5 - PAIR_THREE

0,5 - DIAGONAL_ONE
2,3 - DIAGONAL_TWO

0,4 - DOWN_RIGHT_ONE
1,5 - DOWN_RIGHT_TWO

1,3 - DOWN_LEFT_ONE
2,4 - DOWN_LEFT_TWO

0,1,2,3,4,5 - ALL_ON
0,1,2,3,4,5 - ALL_OFF

0,1,2,3,4,5 - FORWARD
0,1,2,3,4,5 - REVERSE

0,1,2,3,4,5 - OUTSIDE_IN
0,1,2,3,4,5 - INSIDE_OUT

0,1,2,3,4,5 - SPLIT_CHANNELS_ONE
0,1,2,3,4,5 - SPLIT_CHANNELS_TWO

0,1,2,3,4,5 - RANDOM

0,1,2,3,4,5 - END
```

