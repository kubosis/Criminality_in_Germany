{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-24.11";
  };

  outputs = { nixpkgs, ... }:
  let
    pythonKernelName = "sanpy";
    RKernelName = "sanR";
    RKernelDir = "$HOME/.local/share/jupyter/kernels/${RKernelName}";
    system = "x86_64-linux";
    pkgs = nixpkgs.legacyPackages.${system};
    rPackages = with pkgs.rPackages; [
      languageserver
      lintr
      IRkernel
      jsonlite
      BiocManager
      devtools
      Matrix
      factoextra
      DescTools
      ggplot2
      extraDistr
      dplyr
      MASS
      ISLR
      glmnet
      cvTools
      gtools
      caret
      gam
      akima
      mvtnorm
      rcompanion
      scatterplot3d
      Rtsne
      tidyverse
      deldir
      tree
      tsne
      mclust
      cluster
      dbscan
      NMI
      knitr
      elasticnet
      interp
      fastDummies
      FNN
      AER
    ];
    R = pkgs.rWrapper.override { packages = rPackages; };
    RStudio = pkgs.rstudioWrapper.override { packages = rPackages; };
    python = pkgs.python312.withPackages (ps: with ps; [
      ipykernel
      jupyter
      numpy
      pandas
      scipy
      seaborn
      matplotlib
      statsmodels
      scikit-learn
      cvxopt
      scienceplots
    ]);
  in {
    devShells.${system}.default = pkgs.mkShell {
      packages = [
        R
        RStudio
        python
        pkgs.pandoc
      ];

      shellHook = ''
        python -m ipykernel install --user --name=${pythonKernelName}
        mkdir -p "${RKernelDir}"
        echo '{
          "argv": [ "${R}/bin/R", "--slave", "-e", "IRkernel::main()", "--args", "{connection_file}" ],
          "display_name": "${RKernelName}",
          "language": "R"
        }' > "${RKernelDir}/kernel.json"
      '';
    };
  };
}
