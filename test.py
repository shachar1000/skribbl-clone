def spacing(st, n):
    print("".join([" "+x if (index % n == 0) else x for (index, x) in enumerate(st.strip())]))
spacing("hello world sup my man", 1)
