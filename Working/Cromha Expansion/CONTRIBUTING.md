# Menu:
* [Request feature & Report bugs](https://github.com/OcelotWalrus/Cromha-Expansion-plugin/wiki/Contributor-Guide#request-feature--report-bugs)
  * [Reporting bugs](https://github.com/OcelotWalrus/Cromha-Expansion-plugin/wiki/Contributor-Guide#reporting-bugs)
  * [Requesting Features](https://github.com/OcelotWalrus/Cromha-Expansion-plugin/wiki/Contributor-Guide#requesting-features)
* [Adding your own code](https://github.com/OcelotWalrus/Cromha-Expansion-plugin/wiki/Contributor-Guide#adding-your-own-code)
  * [Coding Features & Add-ons](https://github.com/OcelotWalrus/Cromha-Expansion-plugin/wiki/Contributor-Guide#coding-features--add-ons)
    * [Coding Tips](https://github.com/OcelotWalrus/Cromha-Expansion-plugin/wiki/Contributor-Guide#coding-tips)
  * [Apply your code to the base plugin](https://github.com/OcelotWalrus/Cromha-Expansion-plugin/wiki/Contributor-Guide#apply-your-code-to-the-base-plugin)
  * [Using the scripts](https://github.com/OcelotWalrus/Cromha-Expansion-plugin/wiki/Contributor-Guide#using-the-scripts)

# Request feature & Report bugs
**Please, every time before reporting a bug or requesting a feature, check if there is not a duplicated issue(someone that had the same idea or bug than you).**
## Reporting bugs
You can report bugs by opening an issue [here](https://github.com/OcelotWalrus/Cromha-Expansion-plugin/issues/new/choose). Then select the "bug report" option. It will automatically create a pattern to help you making the report clearer. I will try my best to answer you the fastest possible and solve the bug.

It will look like something like this:
![image](https://github.com/OcelotWalrus/Cromha-Expansion-plugin/assets/87318892/ecb3f907-d80b-435d-9a9a-dcccb3962ce6)

Select `Bug Report` and fill in the form that should look like this:
![image](https://github.com/OcelotWalrus/Cromha-Expansion-plugin/assets/87318892/41d5d13b-1268-478f-9f05-74aa3ad89977)

## Requesting Features
You can also request features threw the issues menu on the github repository that you can find [here](https://github.com/OcelotWalrus/Cromha-Expansion-plugin/issues/new/choose). Open an issue and select the "Feature Request" option. It will automatically create a pattern to help you improve your request and make it clearer to us.

It will look like something like this:
![image](https://github.com/OcelotWalrus/Cromha-Expansion-plugin/assets/87318892/ecb3f907-d80b-435d-9a9a-dcccb3962ce6)

Select `Feature Request` and fill in the form that should look like this:
![image](https://github.com/OcelotWalrus/Cromha-Expansion-plugin/assets/87318892/f2d7244c-f487-4378-879f-d0936f71d3c2)

# Adding your own code
First thing first, to contribute to the plugin you have three options: either coding your own idea and create a pull request, either create a feature request but not code it or last, helping on opened bug reports or feature requests.

To check if you can help coding anything, go to the [project](https://github.com/users/OcelotWalrus/projects/5/views/1) and check for issues with the "help wanted" label. You can propose your help here. Even if there is no "help wanted" label, you can still propose your help, all contribution is welcome!

## Coding Features & Add-ons
To code features in the base plugin, you can check the [endless sky github wiki](https://github.com/endless-sky/endless-sky/wiki/CreatingPlugins) to learn how to code things in the [endless sky data format](https://github.com/endless-sky/endless-sky/wiki/DataFormat).

The best way to contribute is [creating a fork](https://docs.github.com/en/get-started/quickstart/fork-a-repo) of the main branch and code in this forked repository.
Note that you can create your own codespace and work on it if you prefer.

**You will find useful links to help you coding faster and better on the [discord server](https://discord.com/invite/tafa8dVH5Q)**

### Coding Tips

Here are some tips to code addons or create your own plugin:
* Always check the "errors.txt" file in your endless sky directory to find possible coding errors made by you or other contributors.

* Be sure to always code stuff that fits good in the base plugin (*in the same "theme" as the base plugin*).

* Keep your code organized in multiple files.

* Add some more details to your addons, to make it more interesting.

* Check the differents projects in the github repositories to know for what we need help or to find some projects that interest you.

* Use the [plugin wiki](https://github.com/OcelotWalrus/Cromha-Expansion-plugin/wiki) as well as the official [plugin creation wiki](https://github.com/endless-sky/endless-sky/wiki#creating-ships-missions-artwork-etc) if there is something you're not sure about.

* If you're adding ships or outfits, make sure that if you made your own model, to add it to the [`source/`](https://github.com/OcelotWalrus/Cromha-Expansion-plugin/tree/main/source) directory. Make sure to use the following pattern for creating files & folders:
```
  source/
  |-- outfit/
  |   |-- <outfit code name>/
  |       |-- 3D/ (the 3D models)
  |       |   |-- <outfit code name>.blend
  |       |       ...
  |       |-- GIMP/ (optional, only if you added metal texture to your render)
  |       |   |-- <outfit code name>.xcf
  |       |       ...
  |       |-- rendering/ (the blender renders in PNG format)
  |       |   |-- raw/ (the render of your blender model without any re-scaling and GIMP modifications)
  |       |   |   |-- <outfit code name>.png
  |       |   |       ...
  |       |   |-- final/ (the render of your blender model with GIMP modifications)
  |       |   |   |-- <outfit code name>.png
  |       |   |       ...
  |       |   |-- sprites/ (the render of your blender model with GIMP modifications and re-scaling for the game)
  |       |       |-- <outfit code name>.png
  |       |           ...
  |       |-- templates/ (optional, only if you use other parts of blender models that are not already in the source/ directory)
  |           ...
  |
  |-- ships/
      |-- <ship code name>/
          |-- 3D/ (the 3D models)
          |   |-- <ship code name>.blend
          |       ...
          |-- GIMP/ (optional, only if you added metal texture to your render)
          |   |-- <ship code name>.xcf
          |   |-- <ship code name>-thumb.xcf
          |       ...
          |-- rendering/ (the blender renders in PNG format)
          |   |-- raw/ (the render of your blender model without any re-scaling and GIMP modifications)
          |   |   |-- <ship code name>.png
          |   |   |-- <ship code name>-thumb.png
          |   |       ...
          |   |-- final/ (the render of your blender model with GIMP modifications)
          |   |   |-- <ship code name>.png
          |   |   |-- <ship code name>-thumb.png
          |   |       ...
          |   |-- sprites/ (the render of your blender model with GIMP modifications and re-scaling for the game)
          |   |   |-- <ship code name>.png
          |   |   |-- <ship code name>-thumb.png
          |   |       ...
          |-- templates/ (optional, only if you use other parts of blender models that are not already in the source/ directory)
              ...
```

_Where <ship code name> is your ship model name without any caps and <outfit code name> is your outfit model name without any caps._

## Apply your code to the base plugin
You can simply create a new [pull request](https://github.com/OcelotWalrus/Cromha-Expansion-plugin/compare) that merge the branch where you created your work (a forked or a local repository of you) to the 'main' branch. If you've done everything right, I or @lumba527 should review the pull request and maybe add your very own code to the plugin.
