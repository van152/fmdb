char __fastcall sub_143D5EA60(__int64 a1, _QWORD *a2, __int64 a3, char a4, char a5)
{
  __int64 v7; // rax
  _QWORD **v8; // rbx
  __int64 v9; // rax
  char v10; // al
  __int64 v11; // rcx

  if ( a5 != 4 && (a4 & 0x20) != 0 || a5 == 4 && (a4 & 0x10) != 0 )
    return 0;
  if ( (a4 & 8) != 0 )
  {
    if ( *a2 != 0 )
    {
      v10 = (*(__int64 (__fastcall **)(_QWORD))(*(_QWORD *)*a2 + 48LL))(*a2);
      v11 = *a2;
      if ( v10 == 17 || *(_DWORD *)(v11 + 12) == -1 )
      {
        v9 = *(int *)(v11 + 8);
        v8 = (_QWORD **)(a3 + 128);
        goto LABEL_17;
      }
    }
    return 0;
  }
  if ( (~a4 & a5) == 0 || *(_BYTE *)(a3 + 89) == 0 )
    return 0;
  v7 = 0;
  if ( **(_QWORD **)(a3 + 128) != *(_QWORD *)(*(_QWORD *)(a3 + 128) + 8LL) && *(int *)a2 >= 0 )
  {
    v8 = (_QWORD **)(a3 + 128);
    LODWORD(v9) = sub_140FFA940(a3);
    if ( (int)v9 < 0 )
    {
      v7 = 0;
      goto LABEL_18;
    }
    v9 = (unsigned int)v9;
LABEL_17:
    v7 = *(_QWORD *)(**v8 + 8 * v9);
  }
LABEL_18:
  *a2 = v7;
  return 1;
}
