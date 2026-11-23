// THUNK ALIAS -> sub_1443D5D60 (jmp:0x1414a1a10->0x1443d5d60)
__int64 __fastcall sub_1443D5D60(__int64 a1, __int64 a2, char a3)
{
  _QWORD *v3; // rax
  unsigned __int8 v7; // bl
  __int64 v8; // rcx
  unsigned int v9; // ecx
  unsigned int v10; // r8d
  int v11; // r9d
  unsigned __int16 v12; // bp
  int v13; // edx
  unsigned __int16 v14; // cx
  bool v15; // cc
  __int64 result; // rax
  _QWORD *v17; // rcx
  _QWORD *v18; // rbp
  __int64 v19; // rax
  __int64 v20; // rcx
  __int64 v21; // rax
  __int64 v22; // rax
  __int64 *v23; // rcx
  __int64 v24; // rax
  __int64 v25; // rcx
  __int64 v26; // rdi
  _QWORD *v27; // rcx
  __int64 v28; // rbp
  unsigned __int64 v29; // rbp
  _DWORD v30[12]; // [rsp+28h] [rbp-30h] BYREF

  v3 = *(_QWORD **)(a1 + 8);
  if ( v3 == nullptr )
    return 0;
  if ( a2 != 0 )
  {
    v7 = a3 & 1;
    if ( (a3 == 0 || v7 != 0) && *(char *)(a1 + 56) > 0 && (*(_BYTE *)(a1 + 59) & 2) == 0 )
    {
      v8 = v3[33];
      if ( v8 != 0 )
      {
        v9 = *(_DWORD *)(v8 + 8);
        v30[0] = v9;
        v10 = HIWORD(v9);
        LOWORD(v11) = HIWORD(dword_141AAE084);
        v12 = (dword_141AAE084 & 0x1FF) - 2;
        if ( (dword_141AAE084 & 0x1FFu) <= 1 )
        {
          v11 = HIWORD(dword_141AAE084) - 1;
          v13 = 3;
          if ( (unsigned __int16)(23593 * v11) < 0xA3Eu )
            v13 = 15;
          v12 += ((v11 & v13) == 0) + 365;
        }
        v14 = v9 & 0x1FF;
        if ( (unsigned __int16)v11 < (unsigned __int16)v10
          || (unsigned __int16)v11 <= (unsigned __int16)v10 && v14 > v12 )
        {
          v15 = (*(char (__fastcall **)(__int64, _DWORD *))(*(_QWORD *)a2 + 408LL))(a2, v30) <= *(_BYTE *)(a1 + 56);
          result = *(unsigned __int8 *)(a1 + 59);
          if ( v15 )
            return 0;
          return result;
        }
      }
    }
    v17 = (_QWORD *)v3[3];
    if ( v17 != (_QWORD *)v3[4] )
    {
      v18 = (_QWORD *)*v17;
      if ( *v17 != 0 && (unsigned __int8)sub_140087070() != 0 )
      {
        v19 = v18[10];
        if ( v18[6] != 0 && v19 != 0 && *(_DWORD *)(v19 + 12) == 40 )
          goto LABEL_57;
        if ( v18[11] != 0 )
          v19 = v18[11];
        if ( v19 != 0 && *(_DWORD *)(v19 + 12) == 40 )
        {
LABEL_57:
          v20 = *(_QWORD *)(v19 + 96);
          if ( v20 != 0 )
          {
            if ( *(_BYTE *)(v19 + 245) == 0 || (v21 = *(_QWORD *)(v20 + 272)) == 0 )
              v21 = *(_QWORD *)(v20 + 264);
            if ( *(char *)(v21 + 1150) >= 0 && (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)a2 + 1728LL))(a2) != 0 )
            {
              v22 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)a2 + 1728LL))(a2);
              v23 = *(__int64 **)(*(int *)(*(_QWORD *)(v22 + 8) + 8LL) + v22 + 96);
              if ( v23 != nullptr && *((_BYTE *)v23 + 75) != 0 )
              {
                v24 = *v23;
                v25 = v23[1];
                if ( v24 != v25 )
                {
                  v26 = 0x200D981001F0LL;
                  do
                  {
                    if ( (unsigned __int8)(*(_BYTE *)(v24 + 11) - 11) <= 1u )
                    {
                      v28 = *(_BYTE *)(v24 + 10) == 4 ? *(_QWORD *)v24 : 0LL;
                      v29 = *(unsigned __int8 *)(v28 + 40);
                      if ( v29 <= 0x2D )
                      {
                        if ( _bittest64(&v26, v29) )
                          return 0;
                      }
                    }
                    v24 += 16;
                  }
                  while ( v24 != v25 );
                }
              }
            }
          }
        }
      }
    }
  }
  else
  {
    v27 = (_QWORD *)v3[3];
    if ( v27 != (_QWORD *)v3[4] && *v27 != 0 )
      sub_140087070();
    v7 = a3 & 1;
  }
  result = 0;
  if ( (v7 | *(_BYTE *)(a1 + 59) & 2) != 0 )
    result = *(unsigned __int8 *)(a1 + 59);
  if ( a3 == 0 )
    return *(unsigned __int8 *)(a1 + 59);
  return result;
}
