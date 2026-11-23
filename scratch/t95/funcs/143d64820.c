char __fastcall sub_143D64820(__int64 a1, _QWORD *a2, char a3)
{
  __int64 v6; // rsi
  __int64 v7; // rbp
  __int64 v8; // rax
  char v9; // al
  __int64 v10; // rcx
  _QWORD **v11; // rsi
  __int64 v12; // rax
  char result; // al
  __int64 *v14; // r8
  __int64 *v15; // rdx
  __int64 *v16; // rcx
  __int64 *v17; // rax
  __int64 v18; // rdi
  __int64 v19; // rsi
  __int64 v20; // rax
  char v21; // al
  __int64 v22; // rcx
  _QWORD **v23; // rdi
  __int64 v24; // rcx
  __int64 *v25; // rdx
  __int64 *v26; // rax
  __int64 *v27; // rcx
  __int64 *v28; // rbp

  v6 = *(_QWORD *)(a1 + 192);
  if ( v6 == 0 )
  {
LABEL_26:
    if ( (a3 & 0x10) == 0 )
    {
      v18 = *(_QWORD *)(a1 + 104);
      if ( (a3 & 8) != 0 )
      {
        if ( *a2 != 0 )
        {
          v21 = (*(__int64 (__fastcall **)(_QWORD))(*(_QWORD *)*a2 + 48LL))(*a2);
          v22 = *a2;
          if ( v21 == 17 || *(_DWORD *)(v22 + 12) == -1 )
          {
            v20 = *(int *)(v22 + 8);
            v23 = (_QWORD **)(v18 + 128);
LABEL_41:
            v24 = *(_QWORD *)(**v23 + 8 * v20);
            *a2 = v24;
            result = 1;
            if ( v24 != 0 )
              *(_BYTE *)(v24 + 26) |= 0x40u;
            return result;
          }
        }
      }
      else if ( (a3 & 4) == 0 && *(_BYTE *)(v18 + 89) != 0 )
      {
        if ( **(_QWORD **)(v18 + 128) != *(_QWORD *)(*(_QWORD *)(v18 + 128) + 8LL) )
        {
          v19 = *a2;
          if ( (int)*a2 >= 0 )
          {
            if ( *(_QWORD *)(v18 + 40) != 0
              || (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v18 + 48LL))(v18) <= (unsigned __int64)(unsigned int)v19 )
            {
              v25 = *(__int64 **)(v18 + 32);
              v26 = (__int64 *)v25[1];
              v27 = v25;
              if ( *((_BYTE *)v26 + 25) == 0 )
              {
                v27 = *(__int64 **)(v18 + 32);
                do
                {
                  v28 = v26 + 2;
                  if ( *((_DWORD *)v26 + 7) >= (int)v19 )
                  {
                    v27 = v26;
                    v28 = v26;
                  }
                  v26 = (__int64 *)*v28;
                }
                while ( *(_BYTE *)(*v28 + 25) == 0 );
              }
              LODWORD(v20) = -1;
              if ( *((_BYTE *)v27 + 25) == 0 && *((_DWORD *)v27 + 7) <= (int)v19 && v27 != v25 )
                LODWORD(v20) = *((_DWORD *)v27 + 8);
            }
            else
            {
              LODWORD(v20) = v19;
            }
            v23 = (_QWORD **)(v18 + 128);
            if ( (int)v20 >= 0 )
            {
              v20 = (unsigned int)v20;
              goto LABEL_41;
            }
          }
        }
        *a2 = 0;
        return 1;
      }
    }
    return 0;
  }
  v7 = *a2;
  if ( (a3 & 0x10) != 0 )
    goto LABEL_25;
  if ( (a3 & 8) != 0 )
  {
    if ( v7 == 0 )
      goto LABEL_25;
    v9 = (*(__int64 (__fastcall **)(_QWORD))(*(_QWORD *)v7 + 48LL))(*a2);
    v10 = *a2;
    if ( v9 != 17 && *(_DWORD *)(v10 + 12) != -1 )
      goto LABEL_25;
    v8 = *(int *)(v10 + 8);
    v11 = (_QWORD **)(v6 + 128);
  }
  else
  {
    if ( (a3 & 4) != 0
      || *(_BYTE *)(v6 + 89) == 0
      || **(_QWORD **)(v6 + 128) == *(_QWORD *)(*(_QWORD *)(v6 + 128) + 8LL)
      || (int)v7 < 0 )
    {
      goto LABEL_25;
    }
    if ( *(_QWORD *)(v6 + 40) != 0
      || (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v6 + 48LL))(v6) <= (unsigned __int64)(unsigned int)v7 )
    {
      v14 = *(__int64 **)(v6 + 32);
      v15 = (__int64 *)v14[1];
      v16 = v14;
      if ( *((_BYTE *)v15 + 25) == 0 )
      {
        v16 = *(__int64 **)(v6 + 32);
        do
        {
          v17 = v15 + 2;
          if ( *((_DWORD *)v15 + 7) >= (int)v7 )
          {
            v16 = v15;
            v17 = v15;
          }
          v15 = (__int64 *)*v17;
        }
        while ( *(_BYTE *)(*v17 + 25) == 0 );
      }
      if ( *((_BYTE *)v16 + 25) != 0 )
        goto LABEL_25;
      if ( *((_DWORD *)v16 + 7) > (int)v7 )
        goto LABEL_25;
      if ( v16 == v14 )
        goto LABEL_25;
      LODWORD(v8) = *((_DWORD *)v16 + 8);
      if ( (int)v8 < 0 )
        goto LABEL_25;
    }
    else
    {
      LODWORD(v8) = v7;
    }
    v11 = (_QWORD **)(v6 + 128);
    v8 = (unsigned int)v8;
  }
  v12 = *(_QWORD *)(**v11 + 8 * v8);
  *a2 = v12;
  if ( v12 == 0 || (*(_BYTE *)(v12 + 26) |= 0x40u, *a2 == 0) || (result = 1, (*(_BYTE *)(*a2 + 27LL) & 4) == 0) )
  {
LABEL_25:
    *a2 = v7;
    goto LABEL_26;
  }
  return result;
}
