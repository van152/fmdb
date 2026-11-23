__int64 __fastcall sub_143C1ED80(_QWORD *a1, char a2, char a3)
{
  int v3; // r9d
  char v4; // r10
  _QWORD *v5; // r11
  __int64 *i; // rcx
  __int64 v7; // rax
  unsigned int v8; // edi
  char v9; // r8
  __int64 **v10; // rdx
  __int64 **v11; // r10
  char v12; // r9
  __int64 result; // rax
  __int64 *v14; // rsi
  __int64 v15; // rcx
  _QWORD *v16; // rax
  int v17; // edi
  int v18; // esi

  v3 = 1049072;
LABEL_2:
  v4 = a3;
  v5 = a1;
  if ( (a2 & 1) != 0 )
  {
    for ( i = (__int64 *)a1[35]; i != (__int64 *)v5[36]; ++i )
    {
      v7 = *i;
      if ( *(_QWORD **)(*i + 8) == v5 )
      {
        v8 = *(unsigned __int8 *)(v7 + 48);
        if ( v8 <= 0x14 )
        {
          if ( _bittest(&v3, v8) )
          {
            a1 = *(_QWORD **)v7;
            a2 = 1;
            a3 = 1;
            if ( *(_QWORD *)v7 != 0 )
              goto LABEL_2;
            break;
          }
        }
      }
    }
  }
  v9 = *(_BYTE *)(v5[32] + 299LL);
  if ( (v4 & 1) == 0 || (v10 = (__int64 **)v5[35], v11 = (__int64 **)v5[36], v10 == v11) )
  {
    v12 = *(_BYTE *)(v5[32] + 299LL);
  }
  else
  {
    v12 = *(_BYTE *)(v5[32] + 299LL);
    do
    {
      v14 = *v10;
      v15 = **v10;
      if ( v15 != 0 )
      {
        v16 = (_QWORD *)v14[1];
        if ( v16 != nullptr )
        {
          v17 = *((unsigned __int8 *)v14 + 48);
          if ( (unsigned int)(v17 - 4) >= 5 && v17 != 20 )
          {
            v18 = *((_DWORD *)v14 + 7);
            if ( (v18 & 0x400) != 0 && v16 == v5 || (v18 & 0x10000) != 0 && v16 == v5 )
            {
              v9 = *(_BYTE *)(*(_QWORD *)(v15 + 256) + 299LL);
              if ( v9 <= 0 )
                v9 = 0;
            }
            if ( v9 > v12 )
              v12 = v9;
          }
        }
      }
      ++v10;
    }
    while ( v10 != v11 );
  }
  result = 0;
  if ( v12 > 0 )
    return (unsigned __int8)v12;
  return result;
}
