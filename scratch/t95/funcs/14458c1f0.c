_DWORD *__fastcall sub_14458C1F0(_DWORD *a1, __int64 a2, __int64 a3)
{
  _DWORD *result; // rax
  unsigned __int64 v4; // r11
  _DWORD *v5; // rax
  _DWORD *v6; // rbp
  _DWORD *v7; // rdi
  _DWORD *v8; // rsi
  _DWORD *v9; // rbx
  _DWORD *v10; // rcx
  int v11; // r13d
  int v12; // ebp
  int v13; // r12d
  int v14; // esi
  int v15; // ebx
  int v16; // edi
  __int64 v17; // r14
  unsigned __int64 v18; // r15
  unsigned __int64 v19; // r15
  __int64 v20; // r10
  __int64 i; // r15
  __int64 v23; // rdi
  _DWORD *v24; // [rsp+8h] [rbp-68h]
  _DWORD *v25; // [rsp+10h] [rbp-60h]
  _DWORD *v26; // [rsp+18h] [rbp-58h]
  _DWORD *v27; // [rsp+20h] [rbp-50h]
  _DWORD *v28; // [rsp+28h] [rbp-48h]

  result = nullptr;
  if ( a2 != 0 && a3 != 0 )
  {
    LOBYTE(v4) = *(_BYTE *)(a3 + 40);
    if ( (_BYTE)v4 == 44 )
    {
      return nullptr;
    }
    else
    {
      v5 = a1 + 4;
      v6 = a1 + 34;
      v7 = a1 + 64;
      v8 = a1 + 94;
      v9 = a1 + 124;
      v10 = a1 + 154;
      v28 = v5;
      v11 = *v5;
      v27 = v6;
      v12 = *v6;
      v26 = v7;
      v13 = *v7;
      v25 = v8;
      v14 = *v8;
      v24 = v9;
      v15 = *v9;
      result = nullptr;
      while ( 1 )
      {
        v16 = *(_DWORD *)(a3 + 12);
        if ( v11 == v16 )
          return v28;
        if ( v12 == v16 )
          return v27;
        if ( v13 == v16 )
          return v26;
        if ( v14 == v16 )
          return v25;
        if ( v15 == v16 )
          return v24;
        if ( *v10 == v16 )
          break;
        if ( (_BYTE)v4 != 22 )
          return result;
        if ( *(_BYTE *)(a2 + 186) != 0 )
          return result;
        v17 = *(_QWORD *)(a2 + 24);
        v18 = (unsigned __int64)(*(_QWORD *)(a2 + 32) - v17) >> 3;
        if ( (int)v18 <= 0 )
          return result;
        v19 = v18 + 0xFFFFFFFF;
        v20 = (unsigned int)v19 + 1LL;
        for ( i = v19 << 56; ; i -= 0x100000000000000LL )
        {
          a3 = *(_QWORD *)(v17 + (i >> 53));
          if ( a3 != 0 )
          {
            v4 = (unsigned int)*(char *)(a3 + 40);
            if ( (unsigned int)v4 <= 0x21 )
            {
              v23 = 0x220263E00LL;
              if ( _bittest64(&v23, v4) )
                break;
            }
          }
          if ( v20-- <= 1 )
            return result;
        }
      }
      return v10;
    }
  }
  return result;
}
