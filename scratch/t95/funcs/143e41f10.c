_QWORD *__fastcall sub_143E41F10(int *a1, _QWORD *a2)
{
  int *v4; // rbx
  __int64 v5; // rcx
  __int64 v6; // rcx
  __int64 v8; // [rsp+30h] [rbp-68h] BYREF
  int v9; // [rsp+38h] [rbp-60h]
  __int64 v10; // [rsp+40h] [rbp-58h] BYREF
  int v11; // [rsp+48h] [rbp-50h]
  __int64 v12[3]; // [rsp+50h] [rbp-48h] BYREF
  _BYTE v13[48]; // [rsp+68h] [rbp-30h] BYREF

  v4 = a1 + 2;
  if ( (*(unsigned __int8 (__fastcall **)(_QWORD, int *))(**((_QWORD **)a1 + 1) + 8LL))(*((_QWORD *)a1 + 1), a1 + 2) != 0 )
  {
    (*(void (__fastcall **)(_QWORD, int *, _BYTE *))(**((_QWORD **)a1 + 1) + 24LL))(*((_QWORD *)a1 + 1), v4, v13);
    v9 = *a1;
    v8 = sub_14083D4F0(v6) + 40;
    sub_140834550((unsigned int)v12, 1685218662, (unsigned int)&v8, 1684237940, (__int64)v13);
  }
  else
  {
    v11 = *a1;
    v10 = sub_14083D4F0(v5) + 40;
    sub_140833C60(v12, 1685218662, &v10);
  }
  sub_14083DDA0(a2, v12);
  sub_140833970(v12);
  return a2;
}
