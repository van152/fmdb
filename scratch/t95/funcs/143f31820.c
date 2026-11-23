char __fastcall sub_143F31820(__int64 a1, __int64 *a2)
{
  __int64 v3; // rax
  __int64 v4; // rdi
  __int64 v5; // rax

  v3 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)a1 + 1032LL))(a1);
  if ( v3 != 0 )
  {
    v4 = v3;
    if ( (*(_BYTE *)(v3 + 28) & 0xFE) == 0x10 )
    {
      if ( a2 != nullptr )
      {
        v5 = *(_QWORD *)(v3 + 16);
LABEL_7:
        *a2 = v5;
      }
      return 1;
    }
    if ( ((*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v3 + 104LL))(v3) & 0xFE) == 0x10 )
    {
      v5 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v4 + 88LL))(v4);
      if ( a2 != nullptr )
        goto LABEL_7;
      return 1;
    }
  }
  return 0;
}
