unsigned __int8 __fastcall sub_143CA00F0(__int64 a1)
{
  unsigned __int8 result; // al
  __int64 v2; // rax
  unsigned __int64 v3; // rax
  __int64 v4; // rcx

  result = 1;
  if ( *(_DWORD *)(a1 + 12) != 150988 )
  {
    v2 = *(_QWORD *)(a1 + 176);
    if ( v2 != 0 )
    {
      return sub_1409CA7C0(*(unsigned __int8 *)(v2 + 572));
    }
    else
    {
      v3 = (unsigned int)*(char *)(a1 + 244);
      if ( (unsigned int)v3 > 0x29 )
      {
        return 0;
      }
      else
      {
        v4 = 0x2018B1F8CC0LL;
        return _bittest64(&v4, v3);
      }
    }
  }
  return result;
}
