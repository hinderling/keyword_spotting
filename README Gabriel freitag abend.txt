This should work for the one-against-all search we want to do. There are some problems I noticed here tho.

I don't think the DTW implementation I used here (from the pyts package) is actually applicable to our problem. 
I came to this conclusion by basically just running the code from this site here (you can actually just look at the 4 graphs): https://pyts.readthedocs.io/en/stable/auto_examples/metrics/plot_dtw.html?highlight=dynamic#sphx-glr-download-auto-examples-metrics-plot-dtw-py

If you look closely at the trajectories of the graphs, you will notice, that they hit the sakoechiba margins. But instead of halting the computation, the DTW just fucking goes on and simply seems to penalize hitting the margin in the DTW distance. which is pretty much the opposite of speeding up computation time. 

the second problem is - we need a way for scoring that actually makes some sense for our application - just summing numbers won't really help us (which is what the library implementations are doing I think) - I was thinking of smth similar to the DNA base pairs aligners were we can give different penalties to insertions/substitutions/whatsoever.

Tomorrow I am going to try to do a DTW myself - the other option would be to hijack some librarie's DTW and adapt it to our needs. I really have no idea what would be faster - Linda told us to use fast DTW - but that is only an approximation afaik so no idea if I would wanna mess with that.