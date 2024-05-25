# What is this?

Place the networks inside this folder. They are ignored by `git` since they are too large to be stored in the repository.

The final structure should look like this:

```
crates_io.net
npm.net
pypi.net
```

## Downloads

### Crates IO

Download from one drive

https://unilj-my.sharepoint.com/:u:/g/personal/jv1721_student_uni-lj_si/EVq1FdT8KeFJunsmw1TnOi4BcjombTz7N-SB9LSsu1EXMg?e=14JPXq

Includes information about:

- Create name
- Number of downloads
- GitHub repository

The direction of edges indicate that the crate depends on the other crate. E.g. `rand --> serde` means that `rand` depends on `serde`.

### NPM

Download from one drive

- full graph (will probably be reduced for processing): https://unilj-my.sharepoint.com/:u:/g/personal/mu6188_student_uni-lj_si/ETlGfP20oqpCpdMlKzUjMgoByzfsCJFu-UcrPWQdrNyKbA?e=CEYBQu

Includes same information as Crates IO, direction of edges is also the same.

### PyPI

Download from one drive

- [full graph](https://unilj-my.sharepoint.com/:u:/g/personal/zt8811_student_uni-lj_si/EftNbN4R6gdBl2MyDfNFaWoBLiYmvm8v0Gjvw6nC3xda0Q?e=fPMolk)

Includes information about:

- Package name
- Number of downloads
