# Nutrition scale

PKU families are taught to weigh food on gram scales and log the measurements for
calculating dietary phenylalanine. Integrating Bluetooth scales with phe-estimation apps
makes logging, and the downstream calculations, seamless and accurate.

I reverse-engineered the Etekcity ESN00 using the methodology in
[this repo](https://github.com/hertzg/metekcity).

Then, using the same process, I added two more Etekcity scales from the FFF0 series.

During the hackathon, I will add two more scales while recording tutorials. Then I will
create an updated tutorial on adding supported scales to PKU Commons.

### The goal

Integrate the scale you already own into the infrastructure where possible, rather than
buying a new one.

## Status

Driver work and the "add your scale" tutorial are tracked in the repo
[`TODO.md`](../TODO.md). Contributions of new scale drivers are welcome.

## Relationship to the benchmark

Accurate gram weights are the input to every phe estimate: `phe = phe-per-gram × grams`.
The weighing captured here feeds the portion term the phe-estimation
[`benchmark/`](../benchmark/) scores. A mis-weighed portion is an estimation error no
matter how good the label parser is.
