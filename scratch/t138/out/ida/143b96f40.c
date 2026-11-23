void __fastcall sub_143B96F40(__int64 a1)
{
  _QWORD *v1; // r15
  char *v3; // r12
  char *v4; // rdi
  char *v5; // rsi
  char *v6; // rsi
  bool v7; // zf
  char *v8; // rbx
  __int64 v9; // rsi
  __int64 v10; // rdi
  unsigned __int16 v11; // cx
  __int64 v12; // rax

  v1 = *(_QWORD **)(a1 + 88);
  if ( v1 == nullptr )
    return;
  v3 = (char *)*v1;
  v4 = (char *)v1[1];
  v5 = v4;
  if ( (char *)*v1 != v4 )
  {
    v6 = v3 + 16;
    while ( (unsigned __int8)sub_141106800(a1: (unsigned __int8)*(v6 - 5)) == 0 )
    {
      v7 = v6 == v4;
      v6 += 16;
      if ( v7 )
      {
        v5 = v4;
        goto LABEL_11;
      }
    }
    v8 = v6 - 16;
    if ( v6 - 16 == v4 || v6 == v4 )
    {
      v5 = v4;
      if ( v8 == v4 )
        goto LABEL_11;
    }
    else
    {
      do
      {
        if ( (unsigned __int8)sub_141106800(a1: (unsigned __int8)v6[11]) == 0 )
        {
          v12 = *(_QWORD *)v6;
          *((_QWORD *)v8 + 1) = *((_QWORD *)v6 + 1);
          *(_QWORD *)v8 = v12;
          v8 += 16;
        }
        v6 += 16;
      }
      while ( v6 != v4 );
      v5 = (char *)v1[1];
      if ( v8 == v4 )
        goto LABEL_11;
    }
    v9 = v5 - v4;
    sub_141758A00(a1: v8, a2: v4, a3: v9);
    v5 = &v8[v9];
    v1[1] = v5;
  }
LABEL_11:
  if ( (char *)(v4 - v3) != &v5[-*v1] )
  {
    v10 = *(_QWORD *)(a1 + 88);
    if ( *(_QWORD *)(v10 + 48) == *(_QWORD *)(v10 + 56) )
    {
      if ( *(_BYTE *)(v10 + 73) == 0xFF )
        goto LABEL_18;
      v11 = word_141AB0260;
      if ( (unsigned __int16)word_141AB0260 >= 0x7E8u )
      {
        word_141AB0260 = 2023;
        v11 = 2023;
      }
      if ( HIWORD(dword_141AAE084) > v11 )
      {
LABEL_18:
        if ( *(_QWORD *)v10 == *(_QWORD *)(v10 + 8)
          && *(_QWORD *)(v10 + 24) == *(_QWORD *)(v10 + 32)
          && *(_BYTE *)(v10 + 72) == 0xFF )
        {
          sub_141400100(a1: v10);
          sub_140DE6D70(a1: v10);
          *(_QWORD *)(a1 + 88) = 0;
        }
      }
    }
  }
}
