_QWORD *__fastcall sub_1438F3740(__int64 a1, _QWORD *a2, __int64 a3)
{
  int v6; // r8d
  int v7; // r9d
  int v8; // ecx
  __int64 v9; // rax
  int v11; // [rsp+A0h] [rbp-38h] BYREF
  int v12; // [rsp+A8h] [rbp-30h] BYREF
  int v13; // [rsp+B0h] [rbp-28h] BYREF
  int v14; // [rsp+B8h] [rbp-20h] BYREF

  v12 = 124518401;
  sub_140931850(a1, &v12, a3, 0);
  v11 = 124518401;
  LOBYTE(v6) = -1;
  LOBYTE(v7) = 1;
  sub_140908040(a1, (unsigned int)&v11, v6, v7, -1);
  if ( (HIWORD(v12) > 0x76Cu || HIWORD(v12) == 1900 && (v12 & 0x1FE) != 0)
    && (HIWORD(v11) > 0x76Cu || HIWORD(v11) == 1900 && (v11 & 0x1FE) != 0) )
  {
    v8 = *(_QWORD *)(qword_141B5AD60 + 8) + 8;
    v9 = *(_QWORD *)(a1 + 288);
    v14 = v11;
    v13 = v12;
    sub_140B47E70(
      v8,
      (_DWORD)a2,
      (unsigned int)&v13,
      (unsigned int)&v14,
      0,
      v9,
      a3,
      0,
      255,
      255,
      0,
      0,
      0,
      0,
      0,
      1,
      1900,
      255,
      0,
      0);
  }
  else
  {
    *a2 = 0;
  }
  return a2;
}
