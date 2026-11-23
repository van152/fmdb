// THUNK ALIAS -> sub_143C29360 (jmp:0x140e626a0->0x143c29360)
__int64 __fastcall sub_143C29360(_QWORD *a1, char a2, char a3)
{
  char v3; // r14
  _QWORD *v4; // rdi
  char v5; // al
  int v6; // r8d
  _QWORD *v7; // rcx
  char v8; // bl
  _QWORD *v9; // rdx
  __int64 *v10; // rsi
  __int64 *v11; // rcx
  __int64 v12; // rbx
  unsigned int v13; // ebp
  unsigned int v14; // ecx
  int v15; // r8d
  _QWORD *v16; // rsi
  __int64 *v17; // rbx
  __int64 *v18; // rdi
  __int64 v19; // rbp
  unsigned int v20; // edx

  v3 = a2;
  v4 = a1;
  v5 = sub_140E60AE0(a1, a2, a3);
  v6 = 1049072;
  v7 = v4;
  v8 = v3;
LABEL_2:
  v9 = v7;
  if ( (v8 & 1) != 0 )
  {
    v10 = (__int64 *)v7[35];
    v11 = (__int64 *)v7[36];
    while ( v10 != v11 )
    {
      v12 = *v10;
      if ( *(_QWORD **)(*v10 + 8) == v9 )
      {
        v13 = *(unsigned __int8 *)(v12 + 48);
        if ( v13 <= 0x14 )
        {
          if ( _bittest(&v6, v13) )
          {
            v7 = *(_QWORD **)v12;
            v8 = 1;
            if ( v7 != nullptr )
              goto LABEL_2;
            break;
          }
        }
      }
      ++v10;
    }
  }
  v14 = *(unsigned __int8 *)(v9[32] + 301LL);
  v15 = 1049072;
LABEL_11:
  v16 = v4;
  if ( (v3 & 1) != 0 )
  {
    v17 = (__int64 *)v4[35];
    v18 = (__int64 *)v4[36];
    while ( v17 != v18 )
    {
      v19 = *v17;
      if ( *(_QWORD **)(*v17 + 8) == v16 )
      {
        v20 = *(unsigned __int8 *)(v19 + 48);
        if ( v20 <= 0x14 )
        {
          if ( _bittest(&v15, v20) )
          {
            v4 = *(_QWORD **)v19;
            v3 = 1;
            if ( *(_QWORD *)v19 != 0 )
              goto LABEL_11;
            break;
          }
        }
      }
      ++v17;
    }
  }
  LOBYTE(v14) = *(_BYTE *)(v16[32] + 300LL) + v5 + v14;
  return v14;
}
