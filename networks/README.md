# What is this?

Extract the networks archive inside this folder. They are ignored by `git` since they are too large to be stored in the repository.

The final structure should look like this:

```
crates_io.graphml
npm.graphml
pypi.graphml
```

## Downloads
Download all networks from [this link](https://unilj-my.sharepoint.com/:u:/g/personal/zt8811_student_uni-lj_si/EXDkJDo5lUdPorlnsuTkqRcB5xBC95r6Wcv8jiZ5J2XPvA?e=J8eiUZ).

### Crates IO

Includes information about:

- Create name
- Number of downloads
- GitHub repository

The direction of edges indicate that the crate depends on the other crate. E.g. `rand --> serde` means that `rand` depends on `serde`.

### NPM

Includes same information as Crates IO, direction of edges is also the same.

### PyPI

Download from one drive

- [full graph](https://unilj-my.sharepoint.com/:u:/g/personal/zt8811_student_uni-lj_si/EftNbN4R6gdBl2MyDfNFaWoBLiYmvm8v0Gjvw6nC3xda0Q?e=fPMolk)

Includes information about:

- Package name
- Number of downloads
