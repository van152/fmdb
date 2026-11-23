__int64 __fastcall sub_1411A41D0(__int64 a1)
{
  __int64 v2; // rdi
  __int64 *v3; // rax
  __int64 v4; // rax
  __int64 v5; // rbx
  __int64 v6; // rcx
  __int64 v7; // rcx
  __int64 *v8; // rax
  __int64 v9; // rax
  __int64 v10; // rsi
  __int64 v11; // rcx
  _QWORD *v12; // rax
  __int64 v13; // r8
  __int64 result; // rax
  _QWORD *v15; // rdi
  __int64 *v16; // rax
  __int64 *v17; // rcx
  int v18; // r8d
  __int64 v19; // rbx
  unsigned int v20; // edx
  __int64 *v21; // rax
  __int64 v22; // rax
  __int64 v23; // rbx
  __int64 v24; // rcx
  __int64 v25; // rcx

  if ( *(_BYTE *)(a1 + 40) == 44 && *(_BYTE *)(a1 + 47) == 0 )
  {
    v2 = *(_QWORD *)(a1 + 48);
    if ( v2 != 0 )
    {
      v3 = *(__int64 **)(v2 + 24);
      if ( v3 != *(__int64 **)(v2 + 32) )
      {
        v4 = *v3;
        if ( v4 != 0 )
        {
          v5 = *(_QWORD *)(v4 + 128);
          if ( v5 != 0 )
          {
            v6 = v5 + *(int *)(*(_QWORD *)(v5 + 8) + 4LL) + 8;
            if ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)v6 + 528LL))(v6) != 0 )
            {
              v7 = v5 + *(int *)(*(_QWORD *)(v5 + 8) + 4LL) + 8;
              if ( (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v7 + 1752LL))(v7) != 0 )
              {
                v8 = *(__int64 **)(v2 + 24);
                if ( v8 != *(__int64 **)(v2 + 32) )
                {
                  v9 = *v8;
                  if ( v9 != 0 )
                  {
                    v10 = *(_QWORD *)(v9 + 128);
                    if ( v10 != 0 )
                    {
                      v11 = v10 + *(int *)(*(_QWORD *)(v10 + 8) + 4LL) + 8;
                      if ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)v11 + 528LL))(v11) != 0 )
                      {
                        v12 = (_QWORD *)(v10 + *(int *)(*(_QWORD *)(v10 + 8) + 4LL) + 8);
                        v13 = 219;
                        return (*(__int64 (__fastcall **)(_QWORD *))(*v12 + 8 * v13))(v12);
                      }
                    }
                  }
                }
                return 0;
              }
            }
          }
        }
      }
    }
  }
  result = *(_QWORD *)(a1 + 128);
  if ( result != 0 )
    return result;
  v15 = *(_QWORD **)(a1 + 48);
  if ( *(_BYTE *)(a1 + 47) != 0 || v15 == nullptr )
    goto LABEL_30;
  v16 = (__int64 *)v15[35];
  v17 = (__int64 *)v15[36];
  if ( v16 == v17 )
    goto LABEL_29;
  v18 = 1049072;
  while ( 1 )
  {
    v19 = *v16;
    if ( *(_QWORD **)(*v16 + 8) == v15 )
    {
      v20 = *(unsigned __int8 *)(v19 + 48);
      if ( v20 <= 0x14 )
      {
        if ( _bittest(&v18, v20) )
          break;
      }
    }
    if ( ++v16 == v17 )
      goto LABEL_29;
  }
  v15 = *(_QWORD **)v19;
  if ( *(_QWORD *)v19 == 0
    || (v21 = (__int64 *)v15[3]) == (__int64 *)v15[4]
    || (v22 = *v21) == 0
    || (v23 = *(_QWORD *)(v22 + 128)) == 0
    || (v24 = v23 + *(int *)(*(_QWORD *)(v23 + 8) + 4LL) + 8,
        (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)v24 + 528LL))(v24) == 0)
    || (v25 = v23 + *(int *)(*(_QWORD *)(v23 + 8) + 4LL) + 8,
        (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v25 + 1752LL))(v25) == 0) )
  {
LABEL_29:
    v15 = *(_QWORD **)(a1 + 48);
LABEL_30:
    if ( v15 == nullptr )
      return 0;
  }
  v12 = (_QWORD *)sub_1411D9CF0((_DWORD)v15, -86, a1, 1, 1);
  if ( v12 != nullptr )
  {
    v13 = 211;
    return (*(__int64 (__fastcall **)(_QWORD *))(*v12 + 8 * v13))(v12);
  }
  return 0;
}
