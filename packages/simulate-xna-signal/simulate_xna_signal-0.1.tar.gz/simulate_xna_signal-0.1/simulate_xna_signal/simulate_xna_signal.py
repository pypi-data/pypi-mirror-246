
import load_kmer_library
import input_4mers
import generate_xplot
import generate_yplot
import plot_signal

KXmer_signal = load_kmer_library.load()

KXmers = input_4mers.input_xna_sequence()

x = generate_xplot.xplot(KXmers)

y = generate_yplot.yplot(KXmer_signal,KXmers)

plot_signal.plot(x,y)



