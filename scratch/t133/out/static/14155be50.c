__int64 __fastcall sub_1444F30B0(_QWORD *a1, _QWORD *a2)
{
  __int64 v4; // rbx
  _QWORD *v5; // r14
  _QWORD *v6; // rbx
  _QWORD *v7; // rdi
  __int64 v8; // rdi
  __int64 v10; // rdi
  __int64 v11; // rbx
  __int64 v12; // rdi
  __int64 v13; // rbp
  _QWORD *v14; // rsi
  __int64 v15; // rcx
  char v16[4]; // [rsp+20h] [rbp-48h] BYREF
  int v17; // [rsp+24h] [rbp-44h] BYREF
  int v18[16]; // [rsp+28h] [rbp-40h] BYREF

  v17 = 0;
  v4 = *a2;
  (*(void (__fastcall **)(_QWORD, int *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v17, a3: 4);
  if ( *(_DWORD *)(v4 + 16) != 0 )
    goto LABEL_9;
  v5 = (_QWORD *)*a1;
  v6 = (_QWORD *)a1[1];
  if ( (_QWORD *)*a1 != v6 )
  {
    v7 = (_QWORD *)*a1;
    do
    {
      if ( *v7 != 0 )
        sub_140ED14E0();
      ++v7;
    }
    while ( v7 != v6 );
    v8 = a1[1] - (_QWORD)v6;
    sub_141758A00(a1: v5, a2: v6, a3: v8);
    a1[1] = (char *)v5 + v8;
  }
  sub_14155CB20(a1: v18, a2, a3: a1, a4: v16);
  if ( v18[0] != 0 )
  {
LABEL_9:
    LODWORD(v5) = 0;
  }
  else
  {
    LOBYTE(v5) = 1;
    if ( v17 <= 2 )
    {
      v10 = a1[1] - *a1;
      if ( v10 != 0 )
      {
        v11 = v10 >> 3;
        v12 = -(__int64)(v10 & 0xFFFFFFFFFFFFFFF8uLL);
        do
        {
          v13 = v11--;
          v14 = (_QWORD *)*a1;
          v15 = *(_QWORD *)(*a1 + 8 * v13 - 8);
          if ( v15 != 0 && *(_BYTE *)(v15 + 4) == 0xAD )
          {
            sub_140ED14E0();
            sub_141758A00(a1: &v14[v13 - 1], a2: &v14[v13], a3: v12 + a1[1] - (_QWORD)v14);
            a1[1] -= 8LL;
          }
          v12 += 8;
        }
        while ( v11 != 0 );
      }
    }
  }
  return (unsigned int)v5;
}
