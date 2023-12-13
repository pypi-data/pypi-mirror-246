import whiledb_rs

print(whiledb_rs.parse("""
/* Can be found at: https://github.com/gzqaq/CS2612-PLaC/tree/main/assigns/assign1202/C/samples */
// sample_src00
n = read_int();
m = n + 1;
write_int(m + 2);
write_char(10);


// sample_src01
n = read_int();
i = 2;
flag = 1;
while (flag && i * i <= n) do {
    if (n % i == 0) then { flag = 0; }
    else { flag = 1; }
    i = i + 1;
}
if (flag) then {
    write_char(80);
    write_char(82);
    write_char(73);
    write_char(77);
    write_char(69);
    write_char(10);
}
else {
    write_char(78);
    write_char(79);
    write_char(78);
    write_char(80);
    write_char(82);
    write_char(73);
    write_char(77);
    write_char(69);
    write_char(10);
}


// sample_src02
n = read_int();
i = 0;
s = 0;
while (i < n) do {
    s = s + read_int();
    i = i + 1;
}
write_int(s);
write_char(10);


// sample_src03
n = read_int();
if (n >= 0) then {
    write_int(n);
}
else {
    write_int(- n);
}
write_char(10);


// sample_src04
n = read_int();
i = 0;
p = 0;
while (i < n) do {
    q = malloc(16);
    * q = read_int();
    * (q + 8) = p;
    p = q;
    i = i + 1;
}
s = 0;
while (p != 0) do {
    s = s + * p;
    p = * (p + 8);
}
write_int(s);
write_char(10);


// sample_src05
n = read_int();
m = - n * n;
m = * n - 1;
write_int(m + 2);


// sample_src06
x = read_int();
if (x > 0) then {
    while (x > 0) do {
        x = x - 1;
    }
}
else {
    if (x < 0) then {
        write_int(0);
    }
    else {
      write_int(1);
    }
}
"""))