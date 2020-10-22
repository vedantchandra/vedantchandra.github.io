---
layout: default
---

<figure>
<img src="{{site.baseurl}}/assets/office.png" alt="office" width="500"/>
</figure>

<h1 id="education">Education</h1>

### [Johns Hopkins University](https://physics-astronomy.jhu.edu/)
Department of Physics and Astronomy <br>
2017-Present: B.S. Physics and Applied Mathematics (Minor in Space Sciences) <br>
Academic Advisors: Professors [Tobias Marriage](https://physics-astronomy.jhu.edu/directory/tobias-marriage/), [Beryl Castello](https://engineering.jhu.edu/ams/faculty/beryl-castello/), and [Charles L. Bennett](https://cosmos.pha.jhu.edu/bennett/).


<h1 id="Research">Research</h1>

I'm interested in a wide range of research topics, a by-product of being easily distracted as a young child. I particularly enjoy working with large datasets, teasing out answers to astrophysical problems with novel statistical techniques. 

<h2 id="wd">White Dwarf Stars</h2>

White dwarfs are the evolutionary end-stages of nearly all stars in the Universe, and exhibit fascinating properties due to their density and composition. There are numerous unsolved problems in white dwarf physics, partly because they have been very difficult to observe in large numbers until recently. 

For the past two years I have been a part of [Professor Nadia Zakamska's](https://zakamska.johnshopkins.edu/main_page.htm) research group, working on characterizing white dwarf atmospheres and inferring their temperatures and surface gravities with spectroscopic measurements. The main challenge is that most current theoretical white dwarf atmospheric models are proprietary and kept under lock and key. Along with graduate student [Hsiang-Chih Hwang](http://www.hwang-astro.me/), we developed a Python package ([wdtools](https://github.com/vedantchandra/wdtools)) that uses various computational techniques to reverse-engineer white dwarf atmospheric models and enable astronomers to predict white dwarf stellar parameters from spectra ([Chandra et al. 2020a](https://ui.adsabs.harvard.edu/abs/2020MNRAS.497.2688C/abstract)). 

Additionally, we recently wrote a paper ([Chandra et al. 2020b](https://ui.adsabs.harvard.edu/abs/2020arXiv200714517C/abstract)) along with graduate student [Sihao Cheng](https://sihaocheng.github.io/) in which we statistically measured the white dwarf mass-radius relation using the gravitational redshift effect. We combined observations of over three thousand white dwarfs from the [Sloan Digital Sky Survey (SDSS)](https://www.sdss.org/) and the [Gaia space observatory](https://sci.esa.int/web/gaia) to average gravitational redshifts as a function of stellar radius, and consequently derived this empirical relation.

<figure>
  <img src="{{site.baseurl}}/assets/mass_radius_photo.png" alt="chandra2020b photometric mass-radius plot" width="500"/>
  <figcaption>The main result from <a href="https://ui.adsabs.harvard.edu/abs/2020arXiv200714517C/abstract">Chandra et al. (2020b)</a>, an observationally-derived white dwarf mass-radius relation across a wide range of stellar masses. Our measurements are in excellent agreement with current theoretical models (overlaid in red and blue).</figcaption>
</figure>

Our work was featured by the [Johns Hopkins HUB](https://hub.jhu.edu/2020/07/30/astrophysicsists-observe-gravitational-redshift-effect/), as well as [the ScienceNews magazine](https://www.sciencenews.org/article/white-dwarf-stars-shrink-size-gain-mass). I wrote a [brief article for *astrobites*](https://astrobites.org/2020/09/28/ur-29-measuring-the-white-dwarf-mass-radius-relation-using-thousands-of-stars/) describing our methods and results. 

<h2 id="rsp">Resolved Stellar Populations</h2>

The vast majority of the galaxies we observe are too faint or distant for us to characterize their individual stars. However, using world-class space telescopes like the Hubble Space Telescope, we can resolve the stellar populations of nearby galaxies and use their color-magnitude diagrams to study their initial mass distribution, composition, and more. It's an open problem in astrophysics whether all galaxies form in a similar fashion to our own Milky Way. The next generation of telescopes like JWST and RST will probe these galaxies deeper than ever before, perhaps finally answering this problem. 

There is a strong need for speedy and accurate techniques to analyse resolved stellar populations to infer parameters that described their formation. I am currently working with [Dr Mario Gennaro](https://www.stsci.edu/stsci-research/research-directory/mario-gennaro) at the Space Telescope Science Institute to develop a computational framework to fit star formation histories and initial mass functions to resolved stellar populations. We are currently building an open-source package ([starwave](https://github.com/vedantchandra/starwave)) to enable the broader astronomical community to perform this kind of analysis.

<h2 id="mpms">The First Stars in the Universe</h2>

The very first stars in the Universe were formed only a hundred million years after the Big Bang in an environment completely devoid of metals - indeed, these primordial stars themselves formed the first metals. It is theorized that some low-mass primordial stars could survive in the local Universe to this day. However, to date they have eluded all efforts to observe them. Instead, astronomers have observed extremely metal-poor stars, which are fascinating in their own right due to their peculiar chemical composition, old age, and insights into Galactic star formation. 

One significant challenge when hunting for metal-poor or metal-free stars is that when observed with spectroscopy, they are nearly indistinguishable from cool white dwarfs. I have recently been working with [Professor Kevin Schlaufman](http://www.kevinschlaufman.com/) on developing an automated technique to differentiate metal-poor main-sequence stars from white dwarfs in large spectroscopic datasets. When applied to future large-scale surveys, this method could help find thousands more extremely metal-poor stars, and provide stronger constraints on the existence of surviving primordial stars in the local Universe. 

<h2 id="hsl">Human Physiology during Long-Duration Spaceflight</h2>

The next few decades will likely see a revolution in manned spaceflight, due to new launch platforms like SpaceX and renewed public interest in sending people to other worlds like the Moon and Mars. The effects of such long-duration spaceflight on human physiology are not yet well understood. Various factors like radiation, lack of gravity, and even loneliness are being actively researched these days. 

I am particularly interested in the effect of spaceflight on the vestibular system or inner ear, which governs balance and orientation. I work with [Professor Mark Shelhamer](https://www.hopkinsmedicine.org/profiles/results/directory/profile/0473514/mark-shelhamer) at the Johns Hopkins School of Medicine to investigate this question using controlled human trials of simulated spaceflight. Along with a large team of student collaborators, we are developing some simple software to analyze physiological signals ([hsltools](https://github.com/vedantchandra/hsltools)) and are in the process of applying it to data we collected on 50 subjects in a spaceflight analog. 

<h1 id="pub">Publications</h1>

<ol start=3 reversed="reversed">
  <li> <b>Chandra, V.</b>, Schlaufman K.C. 2020, <i>Searching for Low-mass Metal-poor Stars Disguised as Cool White Dwarfs</i>, <a href="https://vedantchandra.com/assets/mpms_draft.pdf">submitted to AAS Journals</a></li>

  <li> **Chandra, V.**, Hwang, H.-C., Zakamska, N.L., Cheng, S. 2020, *A Gravitational Redshift Measurement of the White Dwarf Mass-Radius Relation*, [ApJ, 899, 146](https://ui.adsabs.harvard.edu/abs/2020ApJ...899..146C/abstract)</li>

  <li> **Chandra, V.**, Hwang, H.-C., Zakamska, N.L., Budavári, T. 2020, *Computational Tools for the Spectroscopic Analysis of White Dwarfs*, [MNRAS, 497, 2688](https://ui.adsabs.harvard.edu/abs/2020MNRAS.497.2688C/abstract)</li>
</ol>

<h1 id="cv">Curriculum Vitae</h1>

Latest [PDF of my CV]({{site.baseurl}}/assets/cv.pdf). Some additional details are scattered around my [LinkedIn page](https://www.linkedin.com/in/vedant-chandra/). 

<h1 id="contact">Contact Me</h1>

vchandra [at] jhu.edu <br>
(email me for Zoom details) <br>
Twitter: [@vedantchandra](https://twitter.com/vedantchandra) <br>
LinkedIn: [vedant-chandra](https://www.linkedin.com/in/vedant-chandra/) <br>
ORCID: [0000-0002-0572-8012](http://orcid.org/0000-0002-0572-8012)  <br>
Bloomberg Center for Physics and Astronomy, <br>
3400 N Charles St, Baltimore, MD 21218, USA.
