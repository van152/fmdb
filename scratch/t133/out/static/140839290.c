_DWORD *__fastcall sub_143779990(_DWORD *a1, _DWORD *a2, _QWORD *a3)
{
  unsigned int v6; // edx
  int v7; // eax
  unsigned __int64 v8; // rsi
  __int64 v9; // rax
  unsigned int v11; // [rsp+24h] [rbp-1Ch] BYREF
  _QWORD v12[2]; // [rsp+28h] [rbp-18h] BYREF
  int v13; // [rsp+38h] [rbp-8h] BYREF
  unsigned int v14; // [rsp+3Ch] [rbp-4h] BYREF
  __int64 v15; // [rsp+40h] [rbp+0h]

  v15 = -2;
  sub_140835530(a1: a3);
  (*(void (__fastcall **)(_DWORD *, unsigned int *, __int64))(*(_QWORD *)a1 + 40LL))(a1, a2: &v14, a3: 4);
  if ( a1[4] != 0 )
    goto LABEL_14;
  v6 = v14;
  if ( qword_141AA7808 <= (unsigned __int64)v14 )
  {
    a1[4] = 1;
LABEL_14:
    *a2 = 1;
    return a2;
  }
  v7 = 0;
  if ( (__int64)(a3[2] - *a3) >> 4 < (unsigned __int64)v14 )
  {
    sub_140837DD0(a1: a3);
    v6 = v14;
    v7 = a1[4];
  }
  if ( v6 != 0 && v7 == 0 )
  {
    v8 = 1;
    while ( 1 )
    {
      (*(void (__fastcall **)(_DWORD *, unsigned int *, __int64))(*(_QWORD *)a1 + 40LL))(a1, a2: &v11, a3: 4);
      if ( a1[4] != 0 )
        goto LABEL_14;
      v9 = sub_14083D4F0();
      v12[1] = 0;
      v12[0] = v9 + 8;
      sub_1408386A0(a1, a2: &v13, a3: v12);
      if ( v13 != 0 )
      {
        *a2 = 1;
        (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v12[0] + 16LL))(a1: v12[0], a2: v12);
        return a2;
      }
      sub_140833EB0(a1: a3, a2: v11, a3: v12);
      (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v12[0] + 16LL))(a1: v12[0], a2: v12);
      v7 = a1[4];
      if ( v8 < v14 )
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
