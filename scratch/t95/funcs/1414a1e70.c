// THUNK ALIAS -> sub_1443D9CF0 (jmp:0x1414a1e70->0x1443d9cf0)
char __fastcall sub_1443D9CF0(__int64 a1)
{
  __int64 v2; // rcx
  int v3; // edi
  _QWORD *v4; // rax
  unsigned __int8 v5; // bl
  char v6; // cl
  char result; // al
  unsigned int v8; // edi

  v2 = *(_QWORD *)(a1 + 8);
  v3 = *(char *)(v2 + 363);
  v4 = *(_QWORD **)(v2 + 24);
  if ( v4 != *(_QWORD **)(v2 + 32) && *v4 != 0 )
    sub_140087070();
  v5 = *(_BYTE *)(a1 + 59);
  v6 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)a1 + 112LL))(a1);
  result = 1;
  if ( v6 != 1 )
  {
    if ( (_BYTE)v3 != 0xFE || (result = 2, v5 <= 1u) )
    {
      v8 = v3 + 2;
      result = 5;
      if ( v8 <= 4 )
        return v8 + 3;
    }
  }
  return result;
}
