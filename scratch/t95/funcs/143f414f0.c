char __fastcall sub_143F414F0(__int64 a1, __int64 *a2)
{
  __int64 v3; // rax
  _BYTE *v4; // rdi
  __int64 v5; // rax
  __int64 v6; // rbx
  char v7; // al
  char v8; // cl
  char result; // al

  v3 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)a1 + 1032LL))(a1);
  if ( v3 != 0 )
  {
    v4 = (_BYTE *)v3;
    v5 = *(_QWORD *)(v3 + 16);
    if ( v5 != 0 && *(_BYTE *)(v5 + 40) == 0 && (v4[28] & 0xFE) == 0x10 )
      goto LABEL_9;
    v6 = (*(__int64 (__fastcall **)(_BYTE *))(*(_QWORD *)v4 + 88LL))(v4);
    v7 = (*(__int64 (__fastcall **)(_BYTE *))(*(_QWORD *)v4 + 104LL))(v4);
    if ( v6 != 0 )
    {
      v8 = v7 & 0xFE;
      result = 0;
      if ( v8 != 16 || *(_BYTE *)(v6 + 40) != 0 )
        return result;
      v5 = (*(__int64 (__fastcall **)(_BYTE *))(*(_QWORD *)v4 + 88LL))(v4);
LABEL_9:
      if ( a2 != nullptr )
        *a2 = v5;
      return 1;
    }
  }
  return 0;
}
