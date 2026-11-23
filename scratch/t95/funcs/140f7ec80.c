// THUNK ALIAS -> sub_143D5E790 (jmp:0x140f7ec80->0x143d5e790)
char __fastcall sub_143D5E790(__int64 a1, int *a2, __int64 a3, char a4, char a5)
{
  __int64 v6; // rax
  _QWORD **v7; // rdi
  __int64 v8; // rax
  __int64 v9; // rax

  if ( a5 != 4 && (a4 & 0x20) != 0 || a5 == 4 && (a4 & 0x10) != 0 )
    return 0;
  if ( (a4 & 8) != 0 )
  {
    v9 = *(_QWORD *)a2;
    if ( *(_QWORD *)a2 != 0 && *(_DWORD *)(v9 + 12) == -1 )
    {
      v8 = *(int *)(v9 + 8);
      v7 = (_QWORD **)(a3 + 128);
      goto LABEL_16;
    }
    return 0;
  }
  if ( (~a4 & a5) == 0 || *(_BYTE *)(a3 + 89) == 0 )
    return 0;
  v6 = 0;
  if ( **(_QWORD **)(a3 + 128) != *(_QWORD *)(*(_QWORD *)(a3 + 128) + 8LL) && *a2 >= 0 )
  {
    v7 = (_QWORD **)(a3 + 128);
    LODWORD(v8) = sub_140FFA940(a3);
    if ( (int)v8 < 0 )
    {
      v6 = 0;
      goto LABEL_17;
    }
    v8 = (unsigned int)v8;
LABEL_16:
    v6 = *(_QWORD *)(**v7 + 8 * v8);
  }
LABEL_17:
  *(_QWORD *)a2 = v6;
  return 1;
}
