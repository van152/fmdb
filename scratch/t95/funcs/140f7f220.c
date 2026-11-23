// THUNK ALIAS -> sub_143D60090 (jmp:0x140f7f220->0x143d60090)
char __fastcall sub_143D60090(__int64 a1, __int64 *a2, char a3)
{
  __int64 v4; // rdi
  __int64 v5; // rax
  __int64 v6; // rbx
  __int64 *v7; // r8
  __int64 *v8; // rax
  __int64 *v9; // rcx
  __int64 *v10; // rdx
  __int64 v11; // rax
  __int64 v13; // rax
  _QWORD **v14; // rdi

  if ( (a3 & 0x20) != 0 )
    return 0;
  v4 = *(_QWORD *)(a1 + 32);
  if ( (a3 & 8) != 0 )
  {
    v11 = *a2;
    if ( *a2 != 0 && *(_DWORD *)(v11 + 12) == -1 )
    {
      v13 = *(int *)(v11 + 8);
      v14 = (_QWORD **)(v4 + 128);
LABEL_20:
      v5 = *(_QWORD *)(**v14 + 8 * v13);
      goto LABEL_21;
    }
    return 0;
  }
  if ( (a3 & 1) != 0 || *(_BYTE *)(v4 + 89) == 0 )
    return 0;
  v5 = 0;
  if ( **(_QWORD **)(v4 + 128) == *(_QWORD *)(*(_QWORD *)(v4 + 128) + 8LL) )
    goto LABEL_21;
  v6 = *a2;
  if ( (int)*a2 < 0 )
    goto LABEL_21;
  if ( *(_QWORD *)(v4 + 40) != 0
    || (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v4 + 48LL))(v4) <= (unsigned __int64)(unsigned int)v6 )
  {
    v7 = *(__int64 **)(v4 + 32);
    v8 = (__int64 *)v7[1];
    v9 = v7;
    if ( *((_BYTE *)v8 + 25) == 0 )
    {
      v9 = *(__int64 **)(v4 + 32);
      do
      {
        v10 = v8 + 2;
        if ( *((_DWORD *)v8 + 7) >= (int)v6 )
        {
          v9 = v8;
          v10 = v8;
        }
        v8 = (__int64 *)*v10;
      }
      while ( *(_BYTE *)(*v10 + 25) == 0 );
    }
    if ( *((_BYTE *)v9 + 25) != 0 )
      goto LABEL_15;
    v5 = 0;
    if ( *((_DWORD *)v9 + 7) > (int)v6 || v9 == v7 )
      goto LABEL_21;
    LODWORD(v6) = *((_DWORD *)v9 + 8);
    if ( (int)v6 < 0 )
    {
LABEL_15:
      v5 = 0;
LABEL_21:
      *a2 = v5;
      return 1;
    }
  }
  v14 = (_QWORD **)(v4 + 128);
  v13 = (unsigned int)v6;
  goto LABEL_20;
}
