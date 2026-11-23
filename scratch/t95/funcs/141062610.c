// THUNK ALIAS -> sub_143EFAFF0 (jmp:0x141062610->0x143efaff0)
bool __fastcall sub_143EFAFF0(__int64 a1)
{
  __int64 v1; // rax
  char v2; // cl
  _BYTE *v3; // rdx
  _BYTE *v4; // rax

  if ( (_BYTE)word_141B60320 == 0 )
    return false;
  v1 = *(_QWORD *)(*(_QWORD *)(a1 + 368) + 288LL);
  if ( v1 == 0 )
    return false;
  v2 = *(_BYTE *)(a1 + 185);
  if ( v2 != 0 )
  {
    v3 = *(_BYTE **)(v1 + 624);
    if ( v3 == nullptr )
      return false;
  }
  else
  {
    v3 = *(_BYTE **)(v1 + 624);
  }
  v4 = (_BYTE *)(v1 + 88);
  if ( v2 != 0 )
    v4 = v3;
  if ( v4 != nullptr && *(_BYTE *)(*(_QWORD *)v4 + 68LL) != 0 )
    return (v4[522] & 0xFD) == 0;
  return false;
}
