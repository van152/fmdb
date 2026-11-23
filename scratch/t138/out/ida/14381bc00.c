bool __fastcall sub_14381BC00(char a1)
{
  unsigned __int64 v2; // rax
  __int64 v3; // rdx

  if ( qword_141B62EF0 == qword_141B62EF8 )
  {
    v2 = (unsigned int)(a1 - 1);
    if ( (unsigned int)v2 >= 0x31 )
      return (unsigned __int8)(a1 - 1) < 0x40u;
    v3 = 0x19C1000011001LL;
    if ( !_bittest64(&v3, v2) )
      return (unsigned __int8)(a1 - 1) < 0x40u;
  }
  else if ( a1 >= 0 && qword_141B62EF8 - qword_141B62EF0 > (unsigned __int64)(unsigned __int8)a1 )
  {
    return *(_BYTE *)(qword_141B62EF0 + (unsigned __int8)a1) != 0;
  }
  return false;
}
