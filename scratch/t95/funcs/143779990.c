_DWORD *__fastcall sub_143779990(_DWORD *a1, _DWORD *a2, _QWORD *a3)
{
  unsigned int v6; // edx
  int v7; // eax
  unsigned __int64 v8; // rsi
  __int64 v9; // rcx
  __int64 v10; // rax
  int v12; // [rsp+24h] [rbp-1Ch] BYREF
  __int64 v13[2]; // [rsp+28h] [rbp-18h] BYREF
  int v14; // [rsp+38h] [rbp-8h] BYREF
  unsigned int v15; // [rsp+3Ch] [rbp-4h] BYREF
  __int64 v16; // [rsp+40h] [rbp+0h]

  v16 = -2;
  sub_140835530(a3);
  (*(void (__fastcall **)(_DWORD *, unsigned int *, __int64))(*(_QWORD *)a1 + 40LL))(a1, &v15, 4);
  if ( a1[4] != 0 )
    goto LABEL_14;
  v6 = v15;
  if ( qword_141AA7808 <= (unsigned __int64)v15 )
  {
    a1[4] = 1;
LABEL_14:
    *a2 = 1;
    return a2;
  }
  v7 = 0;
  if ( (__int64)(a3[2] - *a3) >> 4 < (unsigned __int64)v15 )
  {
    sub_140837DD0(a3, v15);
    v6 = v15;
    v7 = a1[4];
  }
  if ( v6 != 0 && v7 == 0 )
  {
    v8 = 1;
    while ( 1 )
    {
      (*(void (__fastcall **)(_DWORD *, int *, __int64))(*(_QWORD *)a1 + 40LL))(a1, &v12, 4);
      if ( a1[4] != 0 )
        goto LABEL_14;
      v10 = sub_14083D4F0(v9);
      v13[1] = 0;
      v13[0] = v10 + 8;
      sub_1408386A0(a1, &v14, v13);
      if ( v14 != 0 )
      {
        *a2 = 1;
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v13[0] + 16LL))(v13[0], v13);
        return a2;
      }
      sub_140833EB0(a3, v12, v13);
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v13[0] + 16LL))(v13[0], v13);
      v7 = a1[4];
      if ( v8 < v15 )
      {
        ++v8;
        if ( v7 == 0 )
          continue;
      }
      break;
    }
  }
  *a2 = v7;
  return a2;
}
